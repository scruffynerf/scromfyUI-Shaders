---
description: creative p5.js workflow with baking
---
1. Add the "🎨 Creative P5 Render" node.
2. The default sketch or a new one like this works:
```javascript
function setup() {
    createCanvas(512, 512);
}

function draw() {
    background(0);
    fill(255, 0, 150);
    ellipse(mouseX || width/2, mouseY || height/2, 50, 50);
}
```
3. Set the "frames" widget in the node (e.g., to 60).
4. Click the "Bake Animation" button in the node UI.
5. Wait for the progress bar to complete (this captures the frames from your browser).
6. Once "READY" appears, Queue Prompt.
7. The backend will now use the cached frames to produce the final output.
