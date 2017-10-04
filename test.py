#!/usr/bin/python
#coding: utf-8

li = [0,9,4,2,6,8,3,1]

def sort(li):
    for n in range(len(li)):
        if n == 0:
            continue
        for m in range(0, n):
            if li[m] > li[n]:
                li.insert(m, li[n])
                del li[n+1]
                break
    return li
if __name__ == '__main__':
    li = sort(li)
    print li

