// const cassandra = require('cassandra-driver');

// Credit To:
// https://stackoverflow.com/questions/2368784/draw-on-html5-canvas-using-a-mouse

import {DATA_IMAGE_SIZE, MAIN_CANVAS_SIZE, LINE_WIDTH, PREVIEW_IMAGE_SIZE, MAIN_SCALE} from "./constants";

export default class Drawer {

    constructor() {
        this.canvas = document.getElementById('main-canvas');
        this.input = document.getElementById('input');
        this.canvas.width = MAIN_CANVAS_SIZE;
        this.canvas.height = MAIN_CANVAS_SIZE;
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.initialize();
    }

    initialize() {
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.fillRect(0, 0, MAIN_CANVAS_SIZE, MAIN_CANVAS_SIZE);
        this.drawInput();
        $('#output td').text('').removeClass('success');
    }

    onMouseDown(e) {
        this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.getPosition(e.clientX, e.clientY);
    }

    onMouseUp() {
        this.drawing = false;
        this.drawInput();
    }

    onMouseMove(e) {
        if (this.drawing) {
            const curr = this.getPosition(e.clientX, e.clientY);
            this.ctx.lineWidth = LINE_WIDTH;
            this.ctx.lineCap = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(this.prev.x, this.prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            this.ctx.closePath();
            this.prev = curr;
        }
    }

    getPosition(clientX, clientY) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    drawInput() {
        var ctx = this.input.getContext('2d');
        var img = new Image();
        img.onload = () => {
            var inputs = [];
            var small = document.createElement('canvas').getContext('2d');
            small.drawImage(img, 0, 0, img.width, img.height, 0, 0, DATA_IMAGE_SIZE, DATA_IMAGE_SIZE);
            var data = small.getImageData(0, 0, DATA_IMAGE_SIZE, DATA_IMAGE_SIZE).data;
            for (var i = 0; i < DATA_IMAGE_SIZE; i++) {
                for (var j = 0; j < DATA_IMAGE_SIZE; j++) {
                    var n = 4 * (i * DATA_IMAGE_SIZE + j);
                    inputs[i * DATA_IMAGE_SIZE + j] = (data[n] + data[n + 1] + data[n + 2]) / 3;
                    ctx.fillStyle = 'rgb(' + [data[n], data[n + 1], data[n + 2]].join(',') + ')';
                    ctx.fillRect(j * MAIN_SCALE, i * MAIN_SCALE, MAIN_SCALE, MAIN_SCALE);
                }
            }
            if (Math.min(...inputs) === 255) {
                return;
            }
            $.ajax({
                url: '/mnist',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(inputs),
                success: (data) => {
                    for (let i = 0; i < 2; i++) {
                        var max = 0;
                        var max_index = 0;
                        for (let j = 0; j < 10; j++) {
                            var value = Math.round(data.results[i][j] * 1000);
                            if (value > max) {
                                max = value;
                                max_index = j;
                            }
                            var digits = String(value).length;
                            for (var k = 0; k < 3 - digits; k++) {
                                value = '0' + value;
                            }
                            var text = '0.' + value;
                            if (value > 999) {
                                text = '1.000';
                            }
                            $('#output tr').eq(j + 1).find('td').eq(i).text(text);
                        }
                        for (let j = 0; j < 10; j++) {
                            if (j === max_index) {
                                $('#output tr').eq(j + 1).find('td').eq(i).addClass('success');
                            } else {
                                $('#output tr').eq(j + 1).find('td').eq(i).removeClass('success');
                            }
                        }
                    }
                }
            });
        };
        img.src = this.canvas.toDataURL();
    }
}