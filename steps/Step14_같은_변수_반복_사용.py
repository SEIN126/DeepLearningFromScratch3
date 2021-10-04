# -*- coding: utf-8 -*-
"""Step14_같은_변수_반복_사용.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wKMUG90hLE2Hz8T_JNBEFcGh17dru3kp

#Step14 같은 변수 반복 사용
### 현재 구현으로는 동일한 변수를 사용할 시, 동일한 변수라고 인식하지 못하여 제대로된 미분 값을 구할 수 없음.
"""

import numpy as np

class Variable:
  def __init__(self, data):
    self.data = data
    self.grad = None
    self.creator = None
  
  def set_creator(self, func):
    self.creator = func

  def backward(self):
    '''
      여러개의 입출력을 받을 수 있도록 준비.
    '''
    if self.grad is None:
      self.grad = np.ones_like(self.data)

    funcs = [self.creator]     
    while funcs :              
      f = funcs.pop()          
      gys = [output.grad for output in f.outputs] # output의 grad 가져옴
      gxs = f.backward(*gys)                      # gxs를 구함
      if not isinstance(gxs, tuple):
        gxs = (gxs, )

      for x, gx in zip(f.inputs, gxs):            # 구한 역전파를 각 x.grad에 저장
        if x.grad is None:                        # 같은 변수일 경우에는 덮어쓰지 말고 더해주자!
          x.grad = gx
        else:
          x.grad = x.grad + gx

        if x.creator is not None:                 # 계속해서 역전파 수행
          funcs.append(x.creator) 

class Function:
  '''
    가변 길이로 받은 inputs들을 unpack하고, 출력이 tuple 형태가 아닐 경우엔 추가 지원
  '''
  def __call__(self, *inputs):
    xs = [x.data for x in inputs]
    ys = self.forward(*xs) # 언팩
    if not isinstance(ys, tuple): # tuple 형태가 아닐 경우 추가 지원
      ys = (ys,)
    outputs = [Variable(as_array(y)) for y in ys]
    
    for output in outputs:
      output.set_creator(self) 
    
    self.inputs = inputs
    self.outputs= outputs 
    return outputs if len(outputs) > 1 else outputs[0]

  def forward(self, x):
    raise NotImplementedError()

  def backward(self, gy):
    raise NotImplementedError()

def as_array(x):
  if np.isscalar(x):
    # x가 np.float64 같은 scalar 타입인지 확인(일반 float도 확인됨)
    return np.array(x)
  return x

class Add(Function):
  def forward(self, x0, x1):
    y = x0 + x1
    return y

  def backward(self, gy):
    '''
      backward 부분 추가
    '''
    return gy, gy

def add(x0, x1):
  return Add()(x0, x1)

x = Variable(np.array(3.0))
y = add(add(x, x), x)
y.backward()
print(x.grad)

"""## 미분값 재설정
#### 같은 변수를 사용하여 '다른' 계산을 할 경우, 앞의 구현으로 인하여 계산이 꼬일 수 있음
"""

# 첫번째 계산
x = Variable(np.array(3.0))
y = add(x, x)
y.backward()
print(x.grad) # 3

# 두번째 계산(같은 x를 사용하여 다른 계산을 수행)
y = add(add(x, x), x)
y.backward()
print(x.grad) # 5 -> '3'이 나와야하는데, 첫 번째 연산과 같은 변수의 사용으로, 미분 값이 중첩되어버림

class Variable:
  def __init__(self, data):
    self.data = data
    self.grad = None
    self.creator = None
  
  def set_creator(self, func):
    self.creator = func

  def backward(self):
    '''
      여러개의 입출력을 받을 수 있도록 준비.
    '''
    if self.grad is None:
      self.grad = np.ones_like(self.data)

    funcs = [self.creator]     
    while funcs :              
      f = funcs.pop()          
      gys = [output.grad for output in f.outputs] # output의 grad 가져옴
      gxs = f.backward(*gys)                      # gxs를 구함
      if not isinstance(gxs, tuple):
        gxs = (gxs, )

      for x, gx in zip(f.inputs, gxs):            # 구한 역전파를 각 x.grad에 저장
        if x.grad is None:                        # 같은 변수일 경우에는 덮어쓰지 말고 더해주자!
          x.grad = gx
        else:
          x.grad = x.grad + gx

        if x.creator is not None:                 # 계속해서 역전파 수행
          funcs.append(x.creator) 
  
  def cleargrad(self):
    '''Variable class의 미분값을 초기화 해줌
    '''
    self.grad = None

# 첫번째 계산
x = Variable(np.array(3.0))
y = add(x, x)
y.backward()
print(x.grad) # 3

# 두번째 계산(같은 x를 사용하여 다른 계산을 수행)
x.cleargrad()
y = add(add(x, x), x)
y.backward()
print(x.grad) # 3 -> x.cleargrad()로 인하여 x의 grad가 None으로 초기화 됨