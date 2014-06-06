
def main():
    with open('input_2.txt') as f:
        line = f.readline()
        n = int(line)
        print(n)

        import itertools
        matrix = []
        osum = 0
        sym = 0
        sym1 = 0
        sym2 = 0
        for i in range(int(n)):
            row = f.readline()
            row = row.rstrip()
            rw = row.split(' ')
            roww = []
            for j in range(4):
                roww.append(rw[j])
            pryam = 0
            typ = 0
            gost = 0
            why = itertools.permutations(roww,3)

            for i in why:
                a,b,c = i
                a,b,c = sorted((int(a), int(b), int(c),))

                if a+b <=c:
                    continue
                else:
                    # if u need simply to calculate how match triangles can u build
                    osum+=1
                if a**2 + b**2 == c**2:
                    pryam+=1
                else:
                    cosc = (a**2 + b**2 - c**2 )/2*a*b
                    cosb = (a**2 + c**2 - b**2 )/2*a*c
                    cosa = (c**2 + b**2 - a**2 )/2*c*b
                    if cosa <0 or cosb <0 or cosc<0:
                        typ+=1
                    else:
                        gost+=1
            print(pryam//6,gost//6,typ//6)
            sym+=pryam//6
            sym1+= gost//6
            sym2+= typ//6

        print(sym+sym1+sym2)

        print(osum//6)



if __name__ == '__main__':
    main()

