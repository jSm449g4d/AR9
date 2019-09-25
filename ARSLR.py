#save_load_resolver version:0.3.2
#9th

"""
#how to use

from SLR import slr
import tensorflow as tf

sess = tf.Session()
sess.run(tf.global_variables_initializer())
SLR=slr()#<-after define all of tf.Variable etc...
SLR.load(sess)

SLR.cnt+=1000
SLR.save(sess)
"""

import tensorflow as tf
import os

class slr(object):
    def __init__(self,keepMax=2,directry="./sav"):
        print("starting slr")
        self.saver=tf.train.Saver(max_to_keep=keepMax)
        self.dir=directry
        self.cnt=0
    def save(self,sess,filename="savdata"):
        print("start saving")
        if not os.path.exists(self.dir):os.makedirs(self.dir)
        self.saver.save(sess, os.path.join(self.dir,filename + '.model'), global_step=self.cnt)
        print("saved...")
    def load(self,sess):
        print("start loading")
        ckpt = tf.train.get_checkpoint_state(self.dir)
        if ckpt: 
            print("*************exist************")
            self.saver.restore(sess,ckpt.model_checkpoint_path) 
            self.cnt= int(os.path.basename(ckpt.model_checkpoint_path).split('-')[-1])
            print("loaded...save_data_count=",self.cnt)
        else:print("**********notexist**********")

