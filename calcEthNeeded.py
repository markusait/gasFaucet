def calcEthNeeded(gasNeeded, speed):
    if speed == 'fast':
        return (40 * gasNeeded) /  (10 ** 9)
    if speed =='medium':
        return (4 * gasNeeded) /   (10 ** 9)
    if speed == 'slow':
        return (3 * gasNeeded) /   (10 ** 9)
