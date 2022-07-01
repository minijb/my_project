from keras.layers import Layer

class Mish(Layer):
    def __init__(self,**kwargs):
        super(Mish,self).__init__(**kwargs)
        