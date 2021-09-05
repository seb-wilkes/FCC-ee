# FCC-ee
Any research I have taken part in regarding the FCC-ee.

## Tips for implementing
I found filtering most easily done using Regex. For instance: `baseline_data = tfs.read('./reference/twiss_sr.twiss', index='NAME').filter(regex='^B[^P].*', axis=0)` 
which here filters only Dipoles but no BPMs.




The interaction points for a file starting at the RF is: 
`s_ip = [1.09364439196839e+04,1.23170115057373e+04,\
    3.47229249309653e+04,3.61034925170188e+04,\
    5.85094059422472e+04,5.98899735283005e+04,\
    8.22958869535231e+04,8.36764545395765e+04]`
    
And to exclude it, I've done the hard work (where non_ip here is a deep copy of the relevant data):

`
non_ip = non_ip[~((non_ip['S']>s_ip[0]) & (non_ip['S']< s_ip[1])) \
    & ~(((non_ip['S']>s_ip[2]) & (non_ip['S']< s_ip[3]))) \
    & ~(((non_ip['S']>s_ip[4]) & (non_ip['S']< s_ip[5]))) \
        & ~(((non_ip['S']>s_ip[6]) & (non_ip['S']< s_ip[7])))]
`

It is also important to ensure that the differences in file sizes are accounted for. Assuming they start in the same place, an easy way to get over this is to create an overlap (booL) index.
`overlap_array = data_frame.index.isin(baseline_data.index)`
