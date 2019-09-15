import numpy as np
text_lines=np.array([2,34,5])
notkeep_inds=np.array([0])

text_lines=np.delete(text_lines, notkeep_inds, axis=0)
print(text_lines)