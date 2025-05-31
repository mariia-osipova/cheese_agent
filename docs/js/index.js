import { images } from './images.js';

function pick() {
    return images[Math.floor(Math.random() * images.length)];
}

if (images.length > 0) {
    document.body.style.backgroundImage = `url('${pick()}')`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundRepeat = 'no-repeat';
}
