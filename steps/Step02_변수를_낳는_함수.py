import numpy as np
class Variable:
    def __init__(self, data):
        self.data = data

class Function:
  def __call__(self, input):
    '''
    Variable 인스턴스를 입력받아서 Variable 인스턴스를 출력.
    Variable 인스턴스의 실제 data는 Variable.data에 있음.
    '''
    x = input.data
    y = x ** 2
    output = Variable(y)
    return output

x = Variable(np.array(10))
f = Function()
y = f(x)

print(type(y)) # <class '__main__.Variable'>
print(y.data)  # 100

class Function:
    '''
      - 수정 된 Function.
      - 공통 된 기능만 가지고 있음
      - 구체적인 함수는 Function 클래스를 상속한 클래스에서 구현함.
    '''

    def __call__(self, input):
        x = input.data
        y = self.forward(x)  # 구체적인 계산은 forward method에서 함.
        output = Variable(y)
        return output

    def forward(self, x):
        '''
        - 예외를 발생시킴.
        - 이렇게 해두면 Function 클래스의 forward 메서드를 직접 호출한 사람에게
          '이 메소드는 상속하여 구현해야 한다'는 사실을 알려줄 수 있다.
        '''
        raise NotImplementedError()

class Square(Function):
  '''
  - Function을 상속받은 class
  - Fucntion을 상속받았기 때문에 __call__ 메서드는 그대로 계승
  - forward는 overwrite
  '''
  def forward(self, x):
    return x ** 2

x = Variable(np.array(10))
f = Square()
y = f(x)
print(type(y)) # <class '__main__.Variable'>
print(y.data)  # 100