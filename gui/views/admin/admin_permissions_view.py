from nicegui import ui
from dics.security_config import AVAILABLE_MODULES, PERM_READ, PERM_EDIT, PERM_DELETE
from gui.tools.ui_components import confirm_delete_dialog
from i18n import t


def render_permissions_page(auth_manager):
    ui.label(t('perms.title')).classes('w-full text-center text-3xl font-bold mb-6')

    perm_state = {
        'role': None,
        'permissions': {
            mod: {PERM_READ: False, PERM_EDIT: False, PERM_DELETE: False}
            for mod in AVAILABLE_MODULES
        }
    }

    # ── Permissions dialog ───────────────────────────────────────────────────
    with ui.dialog() as perms_dialog, ui.card().classes('w-full max-w-3xl p-6'):
        perm_title = ui.label().classes('text-xl font-bold mb-2')
        perms_inner = ui.column().classes('w-full gap-0')

        with ui.row().classes('w-full justify-end gap-2 mt-6'):
            ui.button(t('common.cancel'), on_click=lambda: perms_dialog.close()).props('flat')
            ui.button(t('perms.save'), on_click=lambda: _save_permissions()).classes('bg-green-600 text-white px-6')

    def _save_permissions():
        role = perm_state['role']
        if not role:
            return
        try:
            for mod, perms in perm_state['permissions'].items():
                auth_manager.set_permissions(
                    role=role, module_name=mod,
                    can_read=int(perms[PERM_READ]),
                    can_write=int(perms[PERM_EDIT]),
                    can_delete=int(perms[PERM_DELETE]),
                )
            ui.notify(t('perms.saved', role=role), type='positive', position='top')
            perms_dialog.close()
        except Exception as e:
            ui.notify(f"{t('common.error')}: {e}", type='negative')

    def open_perms_for_role(role_name: str):
        perm_state['role'] = role_name
        perm_title.set_text(t('perms.perms_for', role=role_name))

        current = auth_manager.get_user_permissions(role_name)
        for mod in AVAILABLE_MODULES:
            mod_p = current.get(mod, {})
            perm_state['permissions'][mod][PERM_READ] = mod_p.get(PERM_READ, False)
            perm_state['permissions'][mod][PERM_EDIT] = mod_p.get(PERM_EDIT, False)
            perm_state['permissions'][mod][PERM_DELETE] = mod_p.get(PERM_DELETE, False)

        perms_inner.clear()
        with perms_inner:
            with ui.row().classes('w-full font-bold border-b-2 border-gray-200 pb-2 bg-gray-50 px-2 rounded-t flex-nowrap'):
                ui.label(t('perms.module')).classes('w-2/5')
                ui.label(t('perms.read')).classes('w-1/5 text-center text-blue-600')
                ui.label(t('perms.write')).classes('w-1/5 text-center text-green-600')
                ui.label(t('perms.delete')).classes('w-1/5 text-center text-red-600')

            for mod_id, mod_name in AVAILABLE_MODULES.items():
                with ui.row().classes('w-full items-center border-b border-gray-100 py-3 px-2 hover:bg-blue-50 flex-nowrap'):
                    ui.label(mod_name).classes('w-2/5 font-medium text-gray-800')

                    with ui.row().classes('w-1/5 justify-center'):
                        cb_r = ui.checkbox('').bind_value(perm_state['permissions'][mod_id], PERM_READ).props('color=blue')
                    with ui.row().classes('w-1/5 justify-center'):
                        cb_w = ui.checkbox('').bind_value(perm_state['permissions'][mod_id], PERM_EDIT).props('color=green')
                    with ui.row().classes('w-1/5 justify-center'):
                        cb_d = ui.checkbox('').bind_value(perm_state['permissions'][mod_id], PERM_DELETE).props('color=red')

                    def _guard(val, action, r=cb_r, w=cb_w, d=cb_d):
                        if action == PERM_READ and not val:
                            w.set_value(False)
                            d.set_value(False)
                        elif action in (PERM_EDIT, PERM_DELETE) and val:
                            r.set_value(True)

                    cb_r.on('update:model-value', lambda e, r=cb_r, w=cb_w, d=cb_d: _guard(e.args, PERM_READ, r, w, d))
                    cb_w.on('update:model-value', lambda e, r=cb_r, w=cb_w, d=cb_d: _guard(e.args, PERM_EDIT, r, w, d))
                    cb_d.on('update:model-value', lambda e, r=cb_r, w=cb_w, d=cb_d: _guard(e.args, PERM_DELETE, r, w, d))

        perms_dialog.open()

    # ── Add-role dialog ──────────────────────────────────────────────────────
    with ui.dialog() as add_role_dialog, ui.card().classes('w-96 p-6'):
        ui.label(t('perms.new_role')).classes('text-xl font-bold mb-4')
        new_name = ui.input(t('perms.role_name')).classes('w-full')
        new_desc = ui.input(t('perms.role_desc')).classes('w-full mb-4')

        with ui.row().classes('w-full justify-end gap-2'):
            ui.button(t('common.cancel'), on_click=lambda: add_role_dialog.close()).props('flat')
            ui.button(t('common.add'), on_click=lambda: _save_new_role()).classes('bg-green-600 text-white')

    def _save_new_role():
        name = new_name.value.strip()
        if not name:
            ui.notify(t('perms.enter_role_name'), type='warning')
            return
        ok, msg = auth_manager.add_role(name, new_desc.value.strip())
        ui.notify(msg, type='positive' if ok else 'negative')
        if ok:
            add_role_dialog.close()
            _refresh_roles()

    # ── Main card with roles table ───────────────────────────────────────────
    with ui.row().classes('w-full justify-center px-4'):
        with ui.card().classes('w-full max-w-4xl p-6 shadow-md'):

            with ui.row().classes('w-full justify-between items-center mb-6'):
                ui.label(t('perms.roles_title')).classes('text-lg font-bold text-gray-700')
                ui.button(t('perms.add_role'), icon='add', on_click=lambda: (
                    new_name.set_value(''),
                    new_desc.set_value(''),
                    add_role_dialog.open(),
                )).classes('bg-green-600 text-white')

            roles_container = ui.column().classes('w-full gap-0')

            async def _delete_role(role_name: str):
                confirmed = await confirm_delete_dialog(t('perms.delete_confirm', role=role_name))
                if confirmed:
                    ok, msg = auth_manager.delete_role(role_name)
                    ui.notify(msg, type='positive' if ok else 'negative')
                    if ok:
                        _refresh_roles()

            def _refresh_roles():
                roles_container.clear()
                roles = auth_manager.get_roles_full()

                with roles_container:
                    with ui.row().classes('w-full font-bold border-b-2 border-gray-300 pb-2 bg-gray-100 px-4 items-center rounded-t'):
                        ui.label(t('perms.role')).classes('w-1/3 text-gray-600 text-sm uppercase tracking-wide')
                        ui.label(t('perms.description')).classes('flex-1 text-gray-600 text-sm uppercase tracking-wide')
                        ui.label(t('common.actions')).classes('w-36 text-center text-gray-600 text-sm uppercase tracking-wide')

                    if not roles:
                        ui.label(t('perms.no_roles')).classes('text-gray-400 text-center py-6')
                        return

                    for role in roles:
                        is_admin = role['name'] == 'admin'
                        with ui.row().classes('w-full items-center border-b border-gray-100 py-3 px-4 hover:bg-slate-50 transition-colors'):
                            with ui.row().classes('w-1/3 items-center gap-2'):
                                ui.icon('shield' if is_admin else 'person_outline', size='sm',
                                        color='amber-8' if is_admin else 'slate')
                                ui.label(role['name']).classes('font-semibold text-gray-800')
                            ui.label(role.get('description') or '—').classes('flex-1 text-gray-500 text-sm')

                            with ui.row().classes('w-36 justify-center gap-1'):
                                (ui.button(icon='settings', on_click=lambda r=role['name']: open_perms_for_role(r))
                                    .props('flat dense color=primary')
                                    .tooltip(t('perms.configure')))

                                del_btn = (
                                    ui.button(icon='delete_outline',
                                              on_click=lambda r=role['name']: _delete_role(r))
                                    .props('flat dense color=negative')
                                    .tooltip(t('perms.delete_role'))
                                )
                                if is_admin:
                                    del_btn.disable()

            _refresh_roles()
