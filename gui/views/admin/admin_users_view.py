import json
from nicegui import ui
from gui.services.auth_manager import AuthManager
from gui.tools.ui_components import ServerPagination
from i18n import t
import config


def render_users_page(auth_manager: AuthManager):
    ui.label(t('users.title')).classes('w-full text-center text-3xl font-bold mb-6')

    roles = auth_manager.get_available_roles()

    status_options = [t('users.status_all'), t('users.status_active'), t('users.status_inactive')]
    status_map = {
        t('users.status_all'): None,
        t('users.status_active'): True,
        t('users.status_inactive'): False,
    }

    # ── Filter state ─────────────────────────────────────────────────────────
    flt = {'search': '', 'role': None, 'status': status_options[0]}

    # ── Add-user dialog ───────────────────────────────────────────────────────
    with ui.dialog() as add_dialog, ui.card().classes('w-96'):
        ui.label(t('users.new_user')).classes('text-xl font-bold mb-4')
        new_username = ui.input(t('users.login')).classes('w-full')
        new_fullname = ui.input(t('users.full_name')).classes('w-full')
        new_password = ui.input(t('users.password')).classes('w-full').props('type=password')
        new_role = ui.select(roles, label=t('users.role'), value='Гість' if 'Гість' in roles else None).classes('w-full mb-4')

        def save_new_user():
            if not new_username.value or not new_password.value:
                ui.notify(t('users.login_password_required'), type='warning')
                return
            ok, msg = auth_manager.create_user(
                new_username.value.strip(), new_password.value,
                new_role.value, new_fullname.value.strip()
            )
            if ok:
                ui.notify(msg, type='positive')
                add_dialog.close()
                apply_filters(reset_page=True)
            else:
                ui.notify(msg, type='negative')

        with ui.row().classes('w-full justify-end gap-2'):
            ui.button(t('common.cancel'), on_click=add_dialog.close).props('flat')
            ui.button(t('common.create'), on_click=save_new_user).classes('bg-blue-600 text-white')

    # ── Change-password dialog ────────────────────────────────────────────────
    pwd_state = {'user_id': None}

    with ui.dialog() as pass_dialog, ui.card().classes('w-96'):
        ui.label(t('users.change_password')).classes('text-xl font-bold mb-4')
        edit_password = ui.input(t('users.new_password')).classes('w-full mb-4').props('type=password autofocus')

        def save_new_password():
            if not edit_password.value:
                ui.notify(t('users.enter_new_password'), type='warning')
                return
            auth_manager.update_password(pwd_state['user_id'], edit_password.value)
            ui.notify(t('users.password_changed'), type='positive')
            pass_dialog.close()

        with ui.row().classes('w-full justify-end gap-2'):
            ui.button(t('common.cancel'), on_click=pass_dialog.close).props('flat')
            ui.button(t('common.save'), on_click=save_new_password).classes('bg-orange-500 text-white')

    # ── Main layout ───────────────────────────────────────────────────────────
    with ui.column().classes('w-full max-w-6xl mx-auto items-stretch'):

        # Filter card
        with ui.card().classes('w-full mb-4 shadow-sm bg-gray-50 p-3'):
            with ui.row().classes('w-full items-end gap-3 flex-wrap'):
                ui.input(t('users.search_placeholder')).bind_value(flt, 'search').classes('w-48')
                ui.select(
                    [None] + roles, label=t('users.role'), clearable=True
                ).bind_value(flt, 'role').classes('w-40')
                ui.select(
                    status_options, label=t('users.status'), value=status_options[0]
                ).bind_value(flt, 'status').classes('w-36')
                search_btn = ui.button(t('common.search'), icon='search',
                                       on_click=lambda: apply_filters(reset_page=True)) \
                    .classes('bg-primary text-white')
                ui.button(t('common.reset'), icon='clear', on_click=lambda: _reset_filters()) \
                    .classes('bg-gray-400 text-white')
                ui.element('div').classes('flex-1')
                ui.button(t('users.add_user'), icon='person_add', on_click=lambda: (
                    new_username.set_value(''), new_fullname.set_value(''),
                    new_password.set_value(''), add_dialog.open()
                )).classes('bg-green-600 text-white')

        # Table (created once; rows updated by apply_filters)
        roles_json = json.dumps(roles)
        columns = [
            {'name': 'id',        'label': 'ID',                    'field': 'id',        'align': 'left'},
            {'name': 'username',  'label': t('users.login'),        'field': 'username',  'align': 'left'},
            {'name': 'full_name', 'label': t('users.full_name'),    'field': 'full_name', 'align': 'left'},
            {'name': 'role',      'label': t('users.role'),         'field': 'role',      'align': 'center'},
            {'name': 'status',    'label': t('users.access'),       'field': 'is_active', 'align': 'center'},
            {'name': '2fa',       'label': t('users.twofa'),        'field': 'use_2fa',   'align': 'center'},
            {'name': 'actions',   'label': t('common.actions'),     'field': 'actions',   'align': 'center'},
        ]
        table = ui.table(columns=columns, rows=[], row_key='id').classes('w-full general-table')

        table.add_slot('body-cell-role', f'''
            <q-td :props="props">
                <q-select
                    :model-value="props.row.role"
                    :options='{roles_json}'
                    dense options-dense borderless
                    @update:model-value="val => {{ props.row.role = val; $parent.$emit('role_changed', props.row) }}"
                />
            </q-td>
        ''')

        table.add_slot('body-cell-2fa', f'''
            <q-td :props="props">
                <div class="flex items-center justify-center gap-1">
                    <q-toggle
                        :model-value="props.row.use_2fa"
                        color="green"
                        @update:model-value="val => {{ props.row.use_2fa = val; $parent.$emit('toggle_2fa', props.row) }}"
                    />
                    <q-icon :name="props.row.email || props.row.phone ? 'contact_mail' : 'warning'"
                            :color="props.row.email || props.row.phone ? 'grey-5' : 'red'" size="sm">
                        <q-tooltip class="bg-grey-9 text-body2">
                            <div v-if="props.row.email || props.row.phone">
                                <div>📧 Email: {{{{ props.row.email || '—' }}}}</div>
                                <div>📱 Signal: {{{{ props.row.phone || '—' }}}}</div>
                            </div>
                            <div v-else class="text-red-300 font-bold">{t('users.no_contacts_for_2fa')}</div>
                        </q-tooltip>
                    </q-icon>
                </div>
            </q-td>
        ''')

        table.add_slot('body-cell-status', '''
            <q-td :props="props">
                <q-toggle
                    :model-value="props.row.is_active"
                    color="green"
                    @update:model-value="val => { props.row.is_active = val; $parent.$emit('toggle_status', props.row) }"
                />
            </q-td>
        ''')

        table.add_slot('body-cell-actions', f'''
            <q-td :props="props">
                <q-btn size="sm" color="orange" icon="key" flat
                       @click="$parent.$emit('change_pwd', props.row.id)">{t('users.password')}</q-btn>
            </q-td>
        ''')

        # Pager
        with ui.row().classes('w-full justify-center mt-2'):
            pager = ServerPagination(
                records_per_page=config.RECORDS_PER_PAGE,
                on_change=lambda: ui.timer(0.1, lambda: apply_filters(reset_page=False), once=True)
            )

    # ── Event handlers ────────────────────────────────────────────────────────
    def _open_password_dialog(user_id):
        pwd_state['user_id'] = user_id
        edit_password.value = ''
        pass_dialog.open()

    def _toggle_status(user):
        if user['username'] == 'admin':
            ui.notify(t('users.cannot_deactivate_admin'), type='warning')
            apply_filters(reset_page=False)
            return
        auth_manager.update_user(user['id'], role=user['role'],
                                  full_name=user['full_name'], is_active=user['is_active'])
        ui.notify(t('users.status_changed', username=user['username']), type='info')
        apply_filters(reset_page=False)

    def _toggle_2fa(user):
        if user.get('use_2fa') and not user.get('email') and not user.get('phone'):
            ui.notify(t('users.twofa_no_contacts', username=user['username']),
                      type='negative', position='top')
            apply_filters(reset_page=False)
            return
        auth_manager.update_user(user['id'], use_2fa=user['use_2fa'])
        key = 'users.twofa_enabled' if user['use_2fa'] else 'users.twofa_disabled'
        ui.notify(t(key, username=user['username']), type='positive')
        apply_filters(reset_page=False)

    def _update_role(user, new_role):
        if user['username'] == 'admin' and new_role != 'admin':
            ui.notify(t('users.admin_must_be_admin'), type='warning')
            apply_filters(reset_page=False)
            return
        auth_manager.update_user(user['id'], role=new_role,
                                  full_name=user['full_name'], is_active=user['is_active'])
        ui.notify(t('users.role_changed', username=user['username'], role=new_role), type='positive')
        apply_filters(reset_page=False)

    table.on('role_changed',  lambda e: _update_role(e.args, e.args['role']))
    table.on('toggle_status', lambda e: _toggle_status(e.args))
    table.on('toggle_2fa',    lambda e: _toggle_2fa(e.args))
    table.on('change_pwd',    lambda e: _open_password_dialog(e.args))

    # ── Filter logic ──────────────────────────────────────────────────────────
    def _reset_filters():
        flt['search'] = ''
        flt['role'] = None
        flt['status'] = status_options[0]
        ui.timer(0.1, lambda: apply_filters(reset_page=True), once=True)

    def apply_filters(reset_page=True):
        search_btn.props('loading')
        if reset_page:
            pager.reset()

        search = flt['search'].strip() or None
        role = flt['role'] or None
        only_active = status_map.get(flt['status'])

        total = auth_manager.count_users(only_active=only_active, search=search, role=role)
        pager.update_total(total)

        users = auth_manager.get_all_users(
            only_active=only_active, search=search, role=role,
            limit=pager.records_per_page, offset=pager.offset,
        )
        table.rows = users
        table.update()
        search_btn.props(remove='loading')

    ui.timer(0.1, lambda: apply_filters(reset_page=True), once=True)
