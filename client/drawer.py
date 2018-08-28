from pyquery import PyQuery as pq
from lxml import etree
import urllib

d = pq(filename='./templates/index.html')

class Drawer:
    def __init__(self):
        self.DATA_IMAGE_SIZE = 28
        self.MAIN_CANVAS_SIZE = 800
        self.LINE_WIDTH = 12
        self.MAIN_SCALE = 5
        self.canvas = d('#main-canvas')
        self.input = d('#input')
        self.canvas.width = self.MAIN_CANVAS_SIZE
        self.canvas.height = self.MAIN_CANVAS_SIZE
        # self.ctx = self.canvas.getContext('2d')
        # self.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        # this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        # this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        # this.initialize();
        # this.prepareData = {};

    def showCanvas(self):
        print(self.canvas)

    def showSize(self):
        print(self.canvas.width)


drawer = Drawer()
drawer.showSize()

# class Drawer {
#
#     initialize() {
#         this.ctx.fillStyle = '#FFFFFF';
#         this.ctx.fillRect(0, 0, this.MAIN_CANVAS_SIZE, this.MAIN_CANVAS_SIZE);
#         this.drawInput();
#         $('#output td').text('').removeClass('success');
#     }
#
#     onMouseDown(e) {
#         this.canvas.style.cursor = 'default';
#         this.drawing = true;
#         this.prev = this.getPosition(e.clientX, e.clientY);
#     }
#
#     onMouseUp() {
#         this.drawing = false;
#         this.drawInput();
#     }
#
#     onMouseMove(e) {
#         if (this.drawing) {
#             const curr = this.getPosition(e.clientX, e.clientY);
#             this.ctx.lineWidth = this.LINE_WIDTH;
#             this.ctx.lineCap = 'round';
#             this.ctx.beginPath();
#             this.ctx.moveTo(this.prev.x, this.prev.y);
#             this.ctx.lineTo(curr.x, curr.y);
#             this.ctx.stroke();
#             this.ctx.closePath();
#             this.prev = curr;
#         }
#     }
#
#     getPosition(clientX, clientY) {
#         const rect = this.canvas.getBoundingClientRect();
#         return {
#             x: clientX - rect.left,
#             y: clientY - rect.top
#         };
#     }
#
#     drawInput() {
#         const ctx = this.input.getContext('2d');
#         const img = new Image();
#         img.onload = () => {
#             const inputs = [];
#             const small = document.createElement('canvas').getContext('2d');
#             small.drawImage(img, 0, 0, img.width, img.height, 0, 0, this.DATA_IMAGE_SIZE, this.DATA_IMAGE_SIZE);
#             const data = small.getImageData(0, 0, this.DATA_IMAGE_SIZE, this.DATA_IMAGE_SIZE).data;
#             for (var i = 0; i < this.DATA_IMAGE_SIZE; i++) {
#                 for (var j = 0; j < this.DATA_IMAGE_SIZE; j++) {
#                     const n = 4 * (i * this.DATA_IMAGE_SIZE + j);
#                     inputs[i * this.DATA_IMAGE_SIZE + j] = (data[n] + data[n + 1] + data[n + 2]) / 3;
#                     ctx.fillStyle = 'rgb(' + [data[n], data[n + 1], data[n + 2]].join(',') + ')';
#                     ctx.fillRect(j * this.MAIN_SCALE, i * this.MAIN_SCALE, this.MAIN_SCALE, this.MAIN_SCALE);
#                 }
#             }
#             if (Math.min(...inputs) === 255) {
#                 return;
#             }
#             $.ajax({
#                 url: '/mnist',
#                 method: 'POST',
#                 contentType: 'application/json',
#                 data: JSON.stringify(inputs),
#                 success: (data) => {
#                     for (let i = 0; i < 2; i++) {
#                         var max = 0;
#                         var max_index = 0;
#                         for (let j = 0; j < 10; j++) {
#                             var value = Math.round(data.results[i][j] * 1000);
#                             if (value > max) {
#                                 max = value;
#                                 max_index = j;
#                             }
#                             var digits = String(value).length;
#                             for (var k = 0; k < 3 - digits; k++) {
#                                 value = '0' + value;
#                             }
#                             var text = '0.' + value;
#                             if (value > 999) {
#                                 text = '1.000';
#                             }
#                             $('#output tr').eq(j + 1).find('td').eq(i).text(text);
#                         }
#
#                         for (let j = 0; j < 10; j++) {
#                             if (j === max_index) {
#                                 $('#output tr').eq(j + 1).find('td').eq(i).addClass('success');
#                             } else {
#                                 $('#output tr').eq(j + 1).find('td').eq(i).removeClass('success');
#                             }
#                         }
#                     }
#                     this.prepareData['prediction'] = data;
#                 }
#
#             });
#             this.prepareData['imgData'] = inputs;
#         };
#         img.src = this.canvas.toDataURL();
#     }
#
#
#     saveFile(e) {
#
#         var a = document.createElement("a");
#         document.body.appendChild(a);
#         a.style = "display: none";
#
#         var json = JSON.stringify(data),
#             blob = new Blob([data], {type: "text/plain;charset=utf-8"}),
#             url = window.URL.createObjectURL(blob);
#         a.href = url;
#         a.download = fileName;
#         a.click();
#         window.URL.revokeObjectURL(url);
#
#         this.savePreparedData(this.prepareData, "data.txt");
#         e.preventDefault();
#     }
#
#     savePreparedData(data, fileName) {
#         var a = document.createElement("a");
#         document.body.appendChild(a);
#         a.style = "display: none";
#
#         var json = JSON.stringify(data),
#             blob = new Blob([data], {type: "text/plain;charset=utf-8"}),
#             url = window.URL.createObjectURL(blob);
#         a.href = url;
#         a.download = fileName;
#         a.click();
#         window.URL.revokeObjectURL(url);
#     }
#
#     save() {
#         var savefile = document.getElementById("savefile");
#         savefile.addEventListener("click", this.saveFile, false)
#     }
#
# }
