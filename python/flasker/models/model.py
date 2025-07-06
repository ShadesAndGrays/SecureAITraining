from abc import ABC, abstractmethod

# + SetModel()
# + loadParameters()
# + trainModel()
# + EvaluateModel(): string
# + extract Parameters() : array
# + saveModel(filepath:string)

class BaseModel(ABC):

  def get_status():
    pass

  @abstractmethod
  def set_parameters(self,param):
    pass

  @abstractmethod
  def train_model(self):
    pass

  @abstractmethod
  def evaluate_model(self):
    pass

  @abstractmethod
  def extract_parameters(self):
    pass

  @abstractmethod
  def save_model(filePath):
    pass