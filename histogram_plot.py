from ggplot import *

x = ggplot(aes(x='factor(cyl)', fill='factor(gear)'), data=mtcars) + geom_bar()
x