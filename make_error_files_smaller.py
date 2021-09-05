#%%
import in_place
import os
'''
This file is intended to make error files smaller, dramatically increasing performance at run time.
Tested and made around a ~2-3x decrease in run time, and did not affect results (as only cleared 0 lines).
REMEMBER: you can comment out things that aren't useful to you, but the template is here if you need it
(IE: feel free to edit it as you see fit)

'''
#%%
os.system('cp ./clean/bkup/ealign_all.err ./clean/ealign_all.err')
with in_place.InPlace('./clean/ealign_all.err', \
        backup='./clean/eal.err') as file: #backup optional
    for line in file:
        #removes DRIFT
        if line[2] == 'D':
            continue
        #removes ROLL
        elif line[2] == 'R':
            continue
        #removes MCV/H and MULTIK
        elif line[2] == 'M':
            continue
        #ignores BPMs, while adding in sliced dipoles
        elif line[2] == 'B' and line[3] != 'P':
            split_line = line.split()
            name = split_line[0][1:-1]
            data = '   '.join(split_line[1:])
            # This is true for SLICE=4; will need to generalise; otherwise you may safely ignore this!!
            suffixes = ['_DEN','_EN','_BO','_EX','_DEX']
            new_line = ''
            for item in suffixes:
                space = ' '*(20-len(name)-len(item))
                new_line += ' "' + name + item + '"' + space \
                     + data + '\n'
            line = new_line
        file.write(line)
        
print("done")