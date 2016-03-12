import pandas
import analysis
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style

matplotlib.style.use('ggplot')
analysis.train.outcome.value_counts().plot(kind='barh')
matplotlib.pyplot.show()

