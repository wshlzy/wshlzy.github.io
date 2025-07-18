function toggleNav(side) {
    var sidebar, toggleBtn;
    if (side === 'left') {
        sidebar = document.getElementById("leftSidebar");
        toggleBtn = document.getElementById("toggleLeftBtn");
    } else {
        sidebar = document.getElementById("rightSidebar");
        toggleBtn = document.getElementById("toggleRightBtn");
    }

    if (sidebar.style.width === "0px") {
        sidebar.style.width = "150px";
        toggleBtn.innerHTML = side === 'left' ? "收起课程单" : "收起章节目录";
    } else {
        sidebar.style.width = "0";
        toggleBtn.innerHTML = side === 'left' ? "展开章节目录" : "展开章节目录";
    }
}

// 页面加载时，默认展开右侧边栏，收起左侧边栏
window.onload = function() {
    document.getElementById("leftSidebar").style.width = "0";
    document.getElementById("rightSidebar").style.width = "150px";
};