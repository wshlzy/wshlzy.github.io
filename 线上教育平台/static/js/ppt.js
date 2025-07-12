function zoomIn() {
    var iframe = document.getElementById('pptIframe');
    var width = iframe.width;
    var height = iframe.height;
    iframe.width = width * 1.1;
    iframe.height = height * 1.1;
}

function zoomOut() {
    var iframe = document.getElementById('pptIframe');
    var width = iframe.width;
    var height = iframe.height;
    iframe.width = width * 0.9;
    iframe.height = height * 0.9;
}