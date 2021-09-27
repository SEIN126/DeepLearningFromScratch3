import numpy as np

class Variable:
    def __init__(self, data):
        self.data = data

class Function:
    '''
      - 공통 된 기능만 가지고 있음
    '''
    def __call__(self, input):
        x = input.data
        y = self.forward(x)  # 구체적인 계산은 forward method에서 함.
        output = Variable(y)
        return output

    def forward(self, x):
        '''
        - 이 메소드는 상속하여 구현해야 한다
        '''
        raise NotImplementedError()

class Square(Function):
  def forward(self, x):
    return x ** 2

class Exp(Function):
  def forward(self, x):
    return np.exp(x)

if __name__ == '__main__':
    A = Square()
    B = Exp()
    C = Square()

    x = Variable(np.array(0.5))
    # Function을 상속받은 클래스들은 출력으로 Variable을 뱉기 때문에, 함수를 연속해서 사용가능하다.
    a = A(x)
    b = B(a)
    y = C(b)
    print(y.data)  # 1.648721270700128