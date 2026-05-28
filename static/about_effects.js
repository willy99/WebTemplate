// /static/about_effects.js
import * as THREE from '/static/three.module.js';

// Функція-помічник для безпечного очікування елемента в DOM
function waitForElement(id, callback) {
    const el = document.getElementById(id);
    if (el) {
        callback(el);
    } else {
        // Якщо елемент ще не з'явився, пробуємо знову на наступному кадрі рендерингу
        requestAnimationFrame(() => waitForElement(id, callback));
    }
}

// ── 1. ЕФЕКТ ХАКЕРСЬКОГО ДРУКУ ─────────────────────────────────────
export function initTypewriter(textRaw) {
    waitForElement('hacker-text', (container) => {
        console.log('>>> Контейнер тексту успішно знайдено через асинхронне очікування!');

        let i = 0;
        container.innerHTML = "";

        // Додаємо стилі для курсора, якщо їх ще немає
        if (!document.getElementById('blink-style')) {
            const style = document.createElement('style');
            style.id = 'blink-style';
            style.innerHTML = `
                @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
                .blink-cursor { animation: blink 1s infinite; color: #4ade80; font-weight: bold; }
            `;
            document.head.appendChild(style);
        }

        function typeWriter() {
            // 1. Спочатку видаляємо старий курсор, якщо він є
            const oldCursor = container.querySelector('.blink-cursor');
            if (oldCursor) {
                oldCursor.remove();
            }

            if (i < textRaw.length) {
                let delay = 30; // Стандартна затримка
                let char = textRaw.charAt(i);

                if (char === '\n') {
                    container.innerHTML += '<br>';
                } else if (char === '\t') {
                    delay = Math.floor(Math.random() * 1000) + 500;
                } else {
                    container.innerHTML += char;
                    delay = Math.floor(Math.random() * 150);
                }

                // 2. Додаємо курсор в кінець поточного тексту
                container.innerHTML += '<span class="blink-cursor">_</span>';

                i++;
                setTimeout(typeWriter, delay);
            } else {
                // Якщо текст закінчився, залишаємо курсор назавжди
                container.innerHTML += '<span class="blink-cursor">_</span>';
            }
        }

        typeWriter();
    });
}

// ── 2. 3D ГРАФІКА THREE.JS ─────────────────────────────────────────

// ── 2. 3D ГРАФІКА THREE.JS (КІБЕР-БІГУН) ───────────────────────────
export function init3DCanvas() {
    waitForElement('3d-canvas', (container) => {
        console.log('>>> [OK] Контейнер 3D знайдено:', container);

        const width = container.clientWidth || 400;
        const height = container.clientHeight || 400;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x000000); // Чорний фон

        const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        camera.position.z = 6;
        camera.position.y = 1;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);

        container.innerHTML = "";
        container.appendChild(renderer.domElement);

        // --- СТВОРЕННЯ БІГУНА (СЗЧ) ---
        const runnerGroup = new THREE.Group();

        const material = new THREE.MeshStandardMaterial({
            color: 0x064e3b, // Темно-зелений
            roughness: 0.2,
            metalness: 0.5,
            flatShading: true
        });

        const wireframeMat = new THREE.LineBasicMaterial({
            color: 0x4ade80, // Неоновий зелений контур
            linewidth: 2
        });

        // Спеціальна функція для кінцівок: зміщуємо центр обертання вгору (у плече/таз)
        function createLimb(w, h, d) {
            const geom = new THREE.BoxGeometry(w, h, d);
            geom.translate(0, -h / 2, 0); // Фокус: тепер вісь обертання не по центру, а зверху!
            const mesh = new THREE.Mesh(geom, material);
            const wireframe = new THREE.LineSegments(new THREE.EdgesGeometry(geom), wireframeMat);
            mesh.add(wireframe);
            return mesh;
        }

        function createPart(geom) {
            const mesh = new THREE.Mesh(geom, material);
            const wireframe = new THREE.LineSegments(new THREE.EdgesGeometry(geom), wireframeMat);
            mesh.add(wireframe);
            return mesh;
        }

        // 1. Тулуб (нахилений вперед)
        const torso = createPart(new THREE.BoxGeometry(0.5, 0.8, 0.25));
        torso.position.y = 0.4;
        torso.rotation.x = 0.2; // Нахил корпусу при бігу
        runnerGroup.add(torso);

        // 2. Голова
        const head = createPart(new THREE.BoxGeometry(0.3, 0.3, 0.3));
        head.position.y = 0.95;
        head.position.z = 0.1;
        runnerGroup.add(head);

        // 3. Руки
        const armL = createLimb(0.15, 0.6, 0.15);
        armL.position.set(0.35, 0.7, 0);
        runnerGroup.add(armL);

        const armR = createLimb(0.15, 0.6, 0.15);
        armR.position.set(-0.35, 0.7, 0);
        runnerGroup.add(armR);

        // 4. Ноги
        const legL = createLimb(0.2, 0.7, 0.2);
        legL.position.set(0.15, 0, 0);
        runnerGroup.add(legL);

        const legR = createLimb(0.2, 0.7, 0.2);
        legR.position.set(-0.15, 0, 0);
        runnerGroup.add(legR);

        // Додаємо на сцену
        scene.add(runnerGroup);
        // -----------------------

        // Освітлення
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight1.position.set(5, 5, 5);
        scene.add(dirLight1);

        // Годинник для анімації
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            // Отримуємо поточний час (швидкість бігу)
            const time = clock.getElapsedTime() * 10;

            // АМПЛІТУДА БІГУ: Руки та ноги рухаються за синусоїдою
            const swing = Math.PI / 3; // Кут маху

            armL.rotation.x = Math.sin(time) * swing;
            armR.rotation.x = Math.sin(time + Math.PI) * swing; // Протифаза

            // Ноги рухаються протилежно до рук
            legL.rotation.x = Math.sin(time + Math.PI) * swing;
            legR.rotation.x = Math.sin(time) * swing;

            // Імітація стрибків при бігу (подвійна частота синуса)
            runnerGroup.position.y = Math.abs(Math.sin(time)) * 0.15 - 0.2;

            // Повільне обертання всієї моделі, щоб розглянути її з усіх боків
            runnerGroup.rotation.y += 0.01;

            renderer.render(scene, camera);
        }

        window.addEventListener('resize', () => {
            const w = container.clientWidth || 400;
            const h = container.clientHeight || 400;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });

        animate();
    });
}


export function init3DCanvas_CAT() {
    waitForElement('3d-canvas', (container) => {
        console.log('>>> [OK] Контейнер 3D знайдено:', container);

        const width = container.clientWidth || 400;
        const height = container.clientHeight || 400;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x000000);

        const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        camera.position.z = 6;
        camera.position.y = 1;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);

        container.innerHTML = "";
        container.appendChild(renderer.domElement);

        // --- СТВОРЕННЯ КОТА ---

        const catGroup = new THREE.Group(); // Група, щоб крутити всього кота цілком

        // Спільні матеріали для всіх частин тіла
        const material = new THREE.MeshStandardMaterial({
            color: 0x064e3b, // Темніший зелений, щоб не різав очі
            roughness: 0.2,
            metalness: 0.5,
            flatShading: true
        });

        const wireframeMat = new THREE.LineBasicMaterial({
            color: 0x4ade80, // Яскравий неоновий зелений (колір хакерського тексту)
            linewidth: 2
        });
        // Функція-помічник для створення "запчастин" кота
        function createPart(geometry, x, y, z, rotZ = 0) {
            const mesh = new THREE.Mesh(geometry, material);
            const wireframe = new THREE.LineSegments(new THREE.EdgesGeometry(geometry), wireframeMat);
            mesh.add(wireframe);
            mesh.position.set(x, y, z);
            mesh.rotation.z = rotZ;
            catGroup.add(mesh);
        }

        // 1. Тулуб
        createPart(new THREE.BoxGeometry(1.6, 0.8, 0.8), 0, 0, 0);

        // 2. Голова
        createPart(new THREE.BoxGeometry(0.7, 0.6, 0.7), 0.9, 0.4, 0);

        // 3. Вуха (Пірамідки - ConeGeometry з 4 гранями)
        const earGeom = new THREE.ConeGeometry(0.15, 0.4, 4);
        createPart(earGeom, 0.9, 0.8, 0.2);  // Ліве вухо
        createPart(earGeom, 0.9, 0.8, -0.2); // Праве вухо

        // 4. Лапи
        const legGeom = new THREE.BoxGeometry(0.2, 0.8, 0.2);
        createPart(legGeom, 0.5, -0.7, 0.3);  // Передня ліва
        createPart(legGeom, 0.5, -0.7, -0.3); // Передня права
        createPart(legGeom, -0.5, -0.7, 0.3); // Задня ліва
        createPart(legGeom, -0.5, -0.7, -0.3);// Задня права

        // 5. Хвіст (піднятий догори під кутом)
        createPart(new THREE.BoxGeometry(0.8, 0.15, 0.15), -1.1, 0.3, 0, Math.PI / 4);


        // ── 6. ЕМОЦІЯ ОБЛИЧЧЯ (Очі, брови, носик) ──
        // Робимо спеціальний матеріал, який не реагує на тіні (світиться)
        const faceMat = new THREE.MeshBasicMaterial({ color: 0x4ade80 });

        // Очі (задоволені дуги ^ ^ )
        // TorusGeometry(радіус, товщина, сегменти_трубки, сегменти_кола, довжина_дуги)
        const eyeGeom = new THREE.TorusGeometry(0.06, 0.015, 8, 16, Math.PI);

        const leftEye = new THREE.Mesh(eyeGeom, faceMat);
        leftEye.position.set(1.26, 0.45, 0.15); // Виносимо трохи вперед за голову (X=1.26)
        leftEye.rotation.y = Math.PI / 2;       // Повертаємо обличчям до камери
        catGroup.add(leftEye);

        const rightEye = new THREE.Mesh(eyeGeom, faceMat);
        rightEye.position.set(1.26, 0.45, -0.15);
        rightEye.rotation.y = Math.PI / 2;
        catGroup.add(rightEye);

        // Брови
        const browGeom = new THREE.BoxGeometry(0.02, 0.02, 0.12);

        const leftBrow = new THREE.Mesh(browGeom, faceMat);
        leftBrow.position.set(1.26, 0.55, 0.15);
        leftBrow.rotation.x = 0.2;  // Грайливий нахил
        catGroup.add(leftBrow);

        const rightBrow = new THREE.Mesh(browGeom, faceMat);
        rightBrow.position.set(1.26, 0.55, -0.15);
        rightBrow.rotation.x = -0.2; // Грайливий нахил
        catGroup.add(rightBrow);

        // Додамо крихітний носик для повноти картини!
        const noseGeom = new THREE.BoxGeometry(0.02, 0.04, 0.06);
        const nose = new THREE.Mesh(noseGeom, faceMat);
        nose.position.set(1.26, 0.35, 0);
        catGroup.add(nose);

        // Додаємо зібраного кота на сцену
        catGroup.position.y = 0.5; // Трохи піднімаємо по центру
        scene.add(catGroup);
        // -----------------------

        // Освітлення
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight1.position.set(5, 5, 5);
        scene.add(dirLight1);

        // Анімація: крутимо цілу групу
        function animate() {
            requestAnimationFrame(animate);
            // Кіт крутиться навколо себе, щоб можна було роздивитися
            catGroup.rotation.y += 0.01;
            catGroup.rotation.x += 0.005; // Можна розкоментувати, якщо хочеш, щоб він перекидався в просторі :)
            renderer.render(scene, camera);
        }

        window.addEventListener('resize', () => {
            const w = container.clientWidth || 400;
            const h = container.clientHeight || 400;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });

        animate();
    });
}