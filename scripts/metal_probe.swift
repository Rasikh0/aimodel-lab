import Metal

if let device = MTLCreateSystemDefaultDevice() {
    print("Metal device: \(device.name)")
    print("  unified memory:      \(device.hasUnifiedMemory)")
    print("  max buffer length:   \(device.maxBufferLength)")
    print("  max threads/group:   \(device.maxThreadsPerThreadgroup)")
    if let q = device.makeCommandQueue() {
        print("  command queue: OK")
        _ = q
    } else {
        print("  command queue: FAILED")
    }
} else {
    print("NO METAL DEVICE — GPU unavailable in this guest")
}