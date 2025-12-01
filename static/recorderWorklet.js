class RecorderProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
    }

    process(inputs) {
        const input = inputs[0];
        if (input && input[0]) {
            // copy channel data to avoid reusing the same buffer
            const float32 = new Float32Array(input[0].length);
            float32.set(input[0]);
            // post the buffer to main thread as a transferable (ArrayBuffer)
            this.port.postMessage(float32.buffer, [float32.buffer]);
        }
        return true;
    }
}

registerProcessor("recorder-processor", RecorderProcessor);
