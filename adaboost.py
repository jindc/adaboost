import sys,math

class binarycd():
    def __init__(self):
        self.v=0
        #self.falserate=1
        #self.islittletrue=True
    def run(self,data,weight):
        keys=map(lambda x:x[0],data)
        maxv=max(keys)
        minv=min(keys)
        print keys,maxv,minv

        minfalserate=1
        g_islittletrue=True
        bestv=minv
        vlist=[ minv + 0.5*i for i in range(int((maxv-minv)/0.5)) ]
        print 'vlist',vlist
        for v in vlist:
            tnum=0
            result=[0] * len(data)
            islittletrue=True
            for i in range (len(data)):
                if i < v :
                    result[i]=1
                else:
                    result[i]=-1
            errsum=0
            for i in range(len(data)):
                if result[i] != data[i][1]:
                    errsum +=weight[i]
            if errsum > 0.5:
                islittletrue=False
                errsum = 1-errsum
            if errsum < minfalserate:
                minfalserate=errsum
                g_islittletrue=islittletrue
                bestv=v
            #print v,errsum,islittletrue    
        self.minfalserate=minfalserate
        self.g_islittletrue=g_islittletrue
        self.bestv = bestv
        print data
        print weight
        print self.minfalserate,self.g_islittletrue,self.bestv
    def forecast(self,x):
        ret = -1
        if x < self.bestv:
            ret = 1
        if not self.g_islittletrue:
            ret *= -1
        return ret    
        
class adaboost():
    def run(self,data,m=3):
        
        weightarr=[1/float(len(data))] * len(data)
        print weightarr
        alphaarr=[0.0] * m
        cdarr=[None] * m
        for i in range(m):
            tmpcd=binarycd()
            tmpcd.run(data,weightarr)
            cdarr[i]=tmpcd
            if tmpcd.minfalserate==0:
                alphaarr[i]=100
                break
            erate=  0.5 * math.log( (1-tmpcd.minfalserate)/tmpcd.minfalserate)
            alphaarr[i]=erate
            print erate
            zm= sum([ weightarr[j]*math.exp(-1 * erate* data[j][1]*tmpcd.forecast(data[j][0]))
                      for j in range(len(data))])
            for j in range(len(data)):
                weightarr[j]=weightarr[j]*math.exp(-1 * erate* data[j][1]*tmpcd.forecast(data[j][0]))/zm
            print weightarr
        self.alphaarr=alphaarr
        self.cdarr=cdarr
        print self.alphaarr
    def forecast(self,x):
        tmp=sum([self.alphaarr[i] * self.cdarr[i].forecast(x)   for i in range(len(self.alphaarr))] )
        ret = 1
        if tmp <0:
            ret = -1
        return ret
if __name__=='__main__':
    print 'welcome to use adaboost'
    data=zip(range(10),(1,1,1,-1,-1,-1,1,1,1,-1))
    print data
    ab =adaboost()
    ab.run(data)
    print '5 forecast',ab.forecast(5)
