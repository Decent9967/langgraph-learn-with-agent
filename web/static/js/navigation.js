// ==================== 导航相关 ====================

function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');

    sidebar.classList.toggle('open');

    // 切换菜单图标
    if (sidebar.classList.contains('open')) {
        menuToggle.classList.add('open');
    } else {
        menuToggle.classList.remove('open');
    }
}

// 折叠/展开导航阶段
function toggleSection(headerElement) {
    const section = headerElement.parentElement;
    section.classList.toggle('collapsed');

    // 保存折叠状态到 localStorage
    const sectionTitle = section.querySelector('.nav-section-title').textContent;
    const isCollapsed = section.classList.contains('collapsed');
    saveSectionState(sectionTitle, isCollapsed);
}

// 折叠/展开主页阶段组
function togglePhaseGroup(headerElement) {
    const phaseGroup = headerElement.parentElement;
    phaseGroup.classList.toggle('collapsed');

    // 保存折叠状态到 localStorage（区分侧边栏和主页）
    const phaseTitle = phaseGroup.querySelector('h3').textContent;
    const isCollapsed = phaseGroup.classList.contains('collapsed');
    saveHomePhaseState(phaseTitle, isCollapsed);
}

// 保存侧边栏导航折叠状态
function saveSectionState(sectionTitle, isCollapsed) {
    try {
        let states = JSON.parse(localStorage.getItem('navSectionStates') || '{}');
        states[sectionTitle] = isCollapsed;
        localStorage.setItem('navSectionStates', JSON.stringify(states));
    } catch (e) {
        console.warn('无法保存导航折叠状态:', e);
    }
}

// 保存主页阶段组折叠状态
function saveHomePhaseState(phaseTitle, isCollapsed) {
    try {
        let states = JSON.parse(localStorage.getItem('homePhaseStates') || '{}');
        states[phaseTitle] = isCollapsed;
        localStorage.setItem('homePhaseStates', JSON.stringify(states));
    } catch (e) {
        console.warn('无法保存主页折叠状态:', e);
    }
}

// 恢复侧边栏导航折叠状态
function restoreSectionStates() {
    try {
        const states = JSON.parse(localStorage.getItem('navSectionStates') || '{}');
        const sections = document.querySelectorAll('.nav-section');

        sections.forEach(section => {
            const sectionTitle = section.querySelector('.nav-section-title').textContent;
            if (states[sectionTitle]) {
                section.classList.add('collapsed');
            }
        });
    } catch (e) {
        console.warn('无法恢复导航折叠状态:', e);
    }
}

// 恢复主页阶段组折叠状态
function restoreHomePhaseStates() {
    try {
        const states = JSON.parse(localStorage.getItem('homePhaseStates') || '{}');
        const phaseGroups = document.querySelectorAll('.phase-group');

        phaseGroups.forEach(group => {
            const phaseTitle = group.querySelector('h3').textContent;
            if (states[phaseTitle]) {
                group.classList.add('collapsed');
            }
        });
    } catch (e) {
        console.warn('无法恢复主页折叠状态:', e);
    }
}

// 点击内容区域关闭侧边栏（移动端）
document.addEventListener('DOMContentLoaded', () => {
    const content = document.querySelector('.content');
    const sidebar = document.getElementById('sidebar');

    if (content && sidebar) {
        content.addEventListener('click', () => {
            if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                document.getElementById('menuToggle').classList.remove('open');
            }
        });
    }

    // 恢复导航折叠状态
    restoreSectionStates();

    // 恢复主页阶段组折叠状态
    restoreHomePhaseStates();
});
