def calcEthNeeded(gasNeeded, speed):
    gas = int(gasNeeded)
    if speed == 'fast':
        return (40 * gas) /  (10 ** 9)
    if speed =='medium':
        return (4 * gas) /   (10 ** 9)
    if speed == 'slow':
        return (3 * gas) /   (10 ** 9)
