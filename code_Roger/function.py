# coding: utf-8
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta, datetime
import scipy
import scipy.stats as stats
import matplotlib.colors as mcolors

def sw_betaplane(lat):
    """
    
    Parameters
    ----------
    lat : numeric
        Latitude in degrees.

    Returns
    -------
    None.

    Adapted from  Phil Morgan's [93-04-20  (morgan@ml.csiro.au)] sw_f.m  by Tom Farrar (10-26-01).
    REFERENCE: 
        S. Pond & G.Pickard  2nd Edition 1986
        Introductory Dynamical Oceanogrpahy
        Pergamon Press Sydney.  ISBN 0-08-028728-X
           
        A.E. Gill 1982. p.597
        "Atmosphere-Ocean Dynamics"
        Academic Press: New York.  ISBN: 0-12-283522-0


    # Tom Farrar, 2020, jfarrar@whoi.edu
    # converted from matlab 2020
    """

    DEG2RAD = np.pi/180 
    OMEGA = 7.292e-5      #s-1   A.E.Gill p.597
    a=6378*10**3;    # equatorial radius in meters, A.E.Gill p.597
    beta = (1/a)*2*OMEGA*np.cos(lat*DEG2RAD);

    return beta

def confid(alpha,nu):
    """
    Computes the upper and lower 100(1-alpha)% confidence limits for 
    a chi-square variate (e.g., alpha=0.05 gives a 95% confidence interval).
    Check values (e.g., Jenkins and Watts, 1968, p. 81) are $\nu/\chi^2_{19;0.025}=0.58$
    and $\nu/\chi^2_{19;0.975}=2.11$ (I get 0.5783 and 2.1333 in MATLAB).
    
   
    Parameters
    ----------
    alpha : numeric
        Number of degrees of freedom
    nu : numeric
        Number of degrees of freedom

    Returns (tuple)
    -------
    lower: lower bound of confidence interval
    upper: upper bound of confidence interval

    # Tom Farrar, 2020, jfarrar@whoi.edu
    # converted from matlab 2020
    # This code was written for MIT 12.805 class
    """
    
    # requires:
    # from scipy import stats
    
    upperv=stats.chi2.isf(1-alpha/2,nu)
    lowerv=stats.chi2.isf(alpha/2,nu)
    lower=nu / lowerv
    upper=nu / upperv
    
    return (lower, upper) # Return tuple; could instead do this as dictionary or list


def new_blues_cb():
    reds = np.array([ 0.9180593 ,  0.912487  ,  0.90691471,  0.90134241,  0.89577012,
            0.89019782,  0.88462553,  0.87905323,  0.87348094,  0.86790864,
            0.86233635,  0.85676405,  0.85119176,  0.84561947,  0.84004717,
            0.83447488,  0.82890258,  0.82333029,  0.81775799,  0.8121857 ,
            0.8066134 ,  0.80104111,  0.79546881,  0.78989652,  0.78432422,
            0.77875193,  0.77317963,  0.76760734,  0.76203504,  0.75646275,
            0.75089046,  0.74531816,  0.73974587,  0.73417357,  0.72860128,
            0.72302898,  0.71745669,  0.71188439,  0.7063121 ,  0.7007398 ,
            0.69516751,  0.68959521,  0.68402292,  0.67845062,  0.67287833,
            0.66730603,  0.66173374,  0.65616145,  0.65058915,  0.64501686,
            0.63944456,  0.63387227,  0.62829997,  0.62272768,  0.61715538,
            0.61158309,  0.60601079,  0.6004385 ,  0.5948662 ,  0.58929391,
            0.58372161,  0.57814932,  0.57257703,  0.56700473,  0.56143244,
            0.55586014,  0.55028785,  0.54471555,  0.53914326,  0.53357096,
            0.52799867,  0.52242637,  0.51685408,  0.51128178,  0.50570949,
            0.50013719,  0.4945649 ,  0.4889926 ,  0.48342031,  0.47784802,
            0.47227572,  0.46670343,  0.46113113,  0.45555884,  0.44998654,
            0.44441425,  0.43884195,  0.43326966,  0.42769736,  0.42212507,
            0.41655277,  0.41098048,  0.40540818,  0.39983589,  0.39426359,
            0.3886913 ,  0.38311901,  0.37754671,  0.37197442,  0.36640212,
            0.36082983,  0.35525753,  0.34968524,  0.34411294,  0.33854065,
            0.33296835,  0.32739606,  0.32182376,  0.31625147,  0.31067917,
            0.30510688,  0.29953459,  0.29396229,  0.28839   ,  0.2828177 ,
            0.27724541,  0.27167311,  0.26610082,  0.26052852,  0.25495623,
            0.24938393,  0.24381164,  0.23823934,  0.23266705,  0.22709475,
            0.22152246,  0.21595016,  0.21037787,  0.20480558,  0.19923328,
            0.19366099,  0.18808869,  0.1825164 ,  0.1769441 ,  0.17137181,
            0.16579951,  0.16022722,  0.15465492,  0.14908263,  0.14351033,
            0.13793804,  0.13236574,  0.12679345,  0.12122116,  0.11564886,
            0.11007657,  0.10450427,  0.09893198,  0.09335968,  0.08778739,
            0.08221509,  0.0766428 ,  0.0710705 ,  0.06549821,  0.06549821,
            0.06552566,  0.06577674,  0.06622677,  0.0668502 ,  0.06763273,
            0.06855375,  0.06959365,  0.07073404,  0.07195782,  0.07324931,
            0.07459424,  0.07597972,  0.07739416,  0.07882726,  0.08026988,
            0.08171394,  0.08315236,  0.08457895,  0.08598831,  0.08737577,
            0.08873731,  0.09006946,  0.09136928,  0.09263427,  0.09386234,
            0.09505173,  0.09620004,  0.09729997,  0.09835742,  0.0993717 ,
            0.10034231,  0.10126892,  0.10215131,  0.10298843,  0.10377192,
            0.10451122,  0.10520656,  0.10585824,  0.10646662,  0.10702392,
            0.10753553,  0.10800528,  0.10843373,  0.10882021,  0.1091557 ,
            0.10945183,  0.10970926,  0.10992866,  0.11009863,  0.11023173,
            0.11032908,  0.11038934,  0.11040471,  0.11038673,  0.11033616,
            0.11024602,  0.11011983,  0.10996353,  0.10977489,  0.10954788,
            0.10929328,  0.10901163,  0.10869133,  0.108346  ,  0.10797639,
            0.10757131,  0.10714289,  0.10669272,  0.10620936,  0.10570551,
            0.10518146,  0.10462727,  0.10405562,  0.10346375,  0.10284688,
            0.10221505,  0.10156203,  0.10089002,  0.10020549,  0.09949804,
            0.09877832,  0.09804493,  0.09729329,  0.09653316,  0.09575619,
            0.094969  ,  0.09417284,  0.09336173,  0.09254608,  0.09171714,
            0.09088232,  0.090041  ,  0.08919013,  0.08833859,  0.08747533,
            0.08661249,  0.08574385,  0.08487294,  0.08400181,  0.08312617,
            0.0822556 ])
    greens = np.array([ 0.9441798 ,  0.94095789,  0.93774038,  0.93452625,  0.93131455,
            0.92810438,  0.9248949 ,  0.92168533,  0.91847494,  0.91526306,
            0.91204906,  0.90883237,  0.90561245,  0.90238881,  0.899161  ,
            0.89592859,  0.89269119,  0.88944845,  0.88620003,  0.88294564,
            0.87968498,  0.87641781,  0.87314387,  0.86986292,  0.86657473,
            0.8632791 ,  0.8599758 ,  0.85666464,  0.85334541,  0.85001791,
            0.84668191,  0.84333724,  0.83998369,  0.83662105,  0.83324911,
            0.82986764,  0.82647642,  0.82307522,  0.81966379,  0.81624189,
            0.81280925,  0.80936562,  0.80591071,  0.80244424,  0.79896592,
            0.79547544,  0.79197249,  0.78845676,  0.78492789,  0.78138555,
            0.7778294 ,  0.77425906,  0.77067417,  0.76707435,  0.76345922,
            0.75982839,  0.75618144,  0.75251799,  0.74883762,  0.74513991,
            0.74142444,  0.73769077,  0.7339385 ,  0.7301672 ,  0.72637645,
            0.72256583,  0.71873493,  0.71488334,  0.71101066,  0.70711649,
            0.70320047,  0.69926217,  0.69530122,  0.69131735,  0.68731025,
            0.68327963,  0.67922522,  0.67514678,  0.67104413,  0.66691708,
            0.66276538,  0.65858902,  0.65438798,  0.65016224,  0.64591186,
            0.6416369 ,  0.6373375 ,  0.63301382,  0.62866605,  0.62429458,
            0.61989976,  0.61548199,  0.61104174,  0.60657953,  0.60209592,
            0.59759159,  0.59306722,  0.58852353,  0.5839613 ,  0.57938135,
            0.57478456,  0.57017185,  0.5655444 ,  0.56090297,  0.55624857,
            0.55158223,  0.54690499,  0.5422179 ,  0.53752203,  0.53281852,
            0.52810881,  0.52339359,  0.51867392,  0.51395086,  0.50922545,
            0.50449872,  0.49977167,  0.49504528,  0.49032052,  0.48559831,
            0.48087955,  0.4761655 ,  0.47145661,  0.46675366,  0.46205743,
            0.45736864,  0.45268799,  0.44801616,  0.44335376,  0.43870139,
            0.43405962,  0.42942898,  0.42480997,  0.42020304,  0.41560865,
            0.41102721,  0.40645908,  0.40190463,  0.39736419,  0.39283807,
            0.38832654,  0.38382989,  0.37934834,  0.37488213,  0.37043147,
            0.36599656,  0.36157758,  0.35717487,  0.35278857,  0.34841867,
            0.34406531,  0.33972863,  0.33540873,  0.33110575,  0.32681981,
            0.322551  ,  0.31829946,  0.3140653 ,  0.30984863,  0.30564956,
            0.30146848,  0.29730529,  0.29316004,  0.28903289,  0.28492398,
            0.28083345,  0.27676148,  0.27270825,  0.26867393,  0.2646588 ,
            0.2606631 ,  0.25668693,  0.25273054,  0.24879421,  0.24487823,
            0.24098289,  0.23710854,  0.23325554,  0.22942427,  0.2256151 ,
            0.22182847,  0.21806485,  0.21432473,  0.21060865,  0.20691717,
            0.2032509 ,  0.19961045,  0.19599648,  0.19240976,  0.18885105,
            0.18532117,  0.18182099,  0.17835141,  0.17491341,  0.17150798,
            0.1681362 ,  0.16479918,  0.16149814,  0.15823432,  0.15500903,
            0.15182361,  0.1486795 ,  0.14557814,  0.14252107,  0.13950986,
            0.13654614,  0.13363161,  0.13076802,  0.12795703,  0.12520039,
            0.12249987,  0.1198572 ,  0.11727411,  0.11475229,  0.11229336,
            0.10989888,  0.10757029,  0.10530889,  0.10311585,  0.10099212,
            0.09893846,  0.09695535,  0.09504303,  0.0932014 ,  0.09143006,
            0.08972821,  0.08809468,  0.08652789,  0.08502593,  0.08358647,
            0.08220684,  0.08088399,  0.07961456,  0.0783949 ,  0.07722111,
            0.07608911,  0.07499465,  0.07393344,  0.07290112,  0.0718934 ,
            0.07090603,  0.06993211,  0.06896804,  0.0680114 ,  0.06705861,
            0.06610638,  0.06515168,  0.06418929,  0.06321115,  0.06222163,
            0.06121879,  0.06020099,  0.05915624,  0.05808842,  0.0570005 ,
            0.05589169])
    blues = np.array([ 1.        ,  0.99777835,  0.99555669,  0.99333504,  0.99111339,
            0.98889173,  0.98667008,  0.98444842,  0.98222677,  0.98000512,
            0.97778346,  0.97556181,  0.97334016,  0.9711185 ,  0.96889685,
            0.96667519,  0.96445354,  0.96223189,  0.96001023,  0.95778858,
            0.95556693,  0.95334527,  0.95112362,  0.94890196,  0.94668031,
            0.94445866,  0.942237  ,  0.94001535,  0.9377937 ,  0.93557204,
            0.93335039,  0.93112873,  0.92890708,  0.92668543,  0.92446377,
            0.92224212,  0.92002047,  0.91779881,  0.91557716,  0.9133555 ,
            0.91113385,  0.9089122 ,  0.90669054,  0.90446889,  0.90224724,
            0.90002558,  0.89780393,  0.89558227,  0.89336062,  0.89113897,
            0.88891731,  0.88669566,  0.88447401,  0.88225235,  0.8800307 ,
            0.87780904,  0.87558739,  0.87336574,  0.87114408,  0.86892243,
            0.86670078,  0.86447912,  0.86225747,  0.86003582,  0.85781416,
            0.85559251,  0.85337085,  0.8511492 ,  0.84892755,  0.84670589,
            0.84448424,  0.84226259,  0.84004093,  0.83781928,  0.83559762,
            0.83337597,  0.83115432,  0.82893266,  0.82671101,  0.82448936,
            0.8222677 ,  0.82004605,  0.81782439,  0.81560274,  0.81338109,
            0.81115943,  0.80893778,  0.80671613,  0.80449447,  0.80227282,
            0.80005116,  0.79782951,  0.79560786,  0.7933862 ,  0.79116455,
            0.7889429 ,  0.78672124,  0.78449959,  0.78227793,  0.78005628,
            0.77783463,  0.77561297,  0.77339132,  0.77116967,  0.76894801,
            0.76672636,  0.7645047 ,  0.76228305,  0.7600614 ,  0.75783974,
            0.75561809,  0.75339644,  0.75117478,  0.74895313,  0.74673147,
            0.74450982,  0.74228817,  0.74006651,  0.73784486,  0.73562321,
            0.73340155,  0.7311799 ,  0.72895825,  0.72673659,  0.72451494,
            0.72229328,  0.72007163,  0.71784998,  0.71784998,  0.71624858,
            0.71462235,  0.71296882,  0.71128535,  0.70956918,  0.70781736,
            0.70602681,  0.70419426,  0.70231628,  0.70038927,  0.69840946,
            0.69637292,  0.69427555,  0.6921131 ,  0.68988119,  0.68757528,
            0.68519075,  0.68272286,  0.68016682,  0.67751781,  0.67477099,
            0.6719216 ,  0.66896489,  0.66589627,  0.66271137,  0.65940606,
            0.6559765 ,  0.65241923,  0.64873121,  0.64490987,  0.64095315,
            0.63685958,  0.6326283 ,  0.62825909,  0.6237524 ,  0.61910933,
            0.61433167,  0.60942183,  0.60438286,  0.59921837,  0.59393251,
            0.58852986,  0.5830154 ,  0.57739441,  0.5716724 ,  0.56585499,
            0.55994789,  0.55395673,  0.54788707,  0.54175028,  0.53555174,
            0.529293  ,  0.52297876,  0.51661336,  0.5102062 ,  0.50377332,
            0.49730374,  0.49080012,  0.48427492,  0.47774457,  0.47119005,
            0.46461293,  0.45805652,  0.45148217,  0.44489464,  0.43833741,
            0.43176498,  0.42520322,  0.41866115,  0.41210346,  0.40559795,
            0.39907853,  0.39259226,  0.38611587,  0.37965796,  0.37322757,
            0.36680604,  0.36042297,  0.35404476,  0.34770888,  0.34137988,
            0.33508977,  0.32881489,  0.32256801,  0.31635122,  0.31014411,
            0.30398848,  0.29781705,  0.29172467,  0.28561838,  0.27955643,
            0.27351646,  0.26747923,  0.26150605,  0.25552177,  0.24958092,
            0.24366409,  0.23773723,  0.23188363,  0.22602364,  0.22017219,
            0.21437716,  0.2085729 ,  0.20278851,  0.19704663,  0.19129533,
            0.18556525,  0.17987258,  0.17416973,  0.16848004,  0.16283083,
            0.15717011,  0.15150562,  0.14589217,  0.14026517,  0.13462392,
            0.12902168,  0.1234176 ,  0.11779608,  0.11217763,  0.10658282,
            0.10096627,  0.09532647,  0.0897075 ,  0.08407772,  0.07841879,
            0.07272874])
    #N = 256
    N = 220
    vals= np.ones((N, 4))
    vals[:, 0] = reds[:N]
    vals[:, 1] = greens[:N]
    vals[:, 2] = blues[:N]
    newcmp = mcolors.ListedColormap(vals[:,:])
    return newcmp