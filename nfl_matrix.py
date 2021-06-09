def collect(user_nfl_input):

    user_nfl_input = int(user_nfl_input) # user input was str
    mean_t_ctrl = 20.1272421546223;
    mean_t_a = 37.6534573633676;
    mean_t_suba = 87.1851320359095;
    mean_t_chron = 28.8749959838002;

    SD_t_ctrl = 13.04547;
    SD_t_a = 47.66992;
    SD_t_suba = 472.48477;
    SD_t_chron = 25.56224;

    nfl_value = list(range(5,5001)); 
    nfl_len = list(range(1, len(nfl_value)));

    import math;
    from decimal import Decimal;

    def normdensity(nfl, mean, sd):
        e_pwr = -(math.pow( (nfl-mean), 2) / (2*math.pow(sd,2)));
        x = (1 / Decimal(2*math.pi*sd)) * Decimal(math.pow(math.e, e_pwr));
        return x;

    norm_density_ctrl = [];
    norm_density_a = [];
    norm_density_suba = [];
    norm_density_chron = [];
    prob_ctrl = [];
    prob_stroke = [];
    like_ratio = [];
    prob_tw_a = [];
    prob_tw_suba = [];
    prob_tw_chron = [];
    ratio_msg = [];

    len_runner = 0;

    for run1 in nfl_value:
        norm_density_ctrl.append(normdensity(run1, mean_t_ctrl, SD_t_ctrl));
        norm_density_a.append(normdensity(run1, mean_t_a, SD_t_a));
        norm_density_suba.append(normdensity(run1, mean_t_suba, SD_t_suba));
        norm_density_chron.append(normdensity(run1, mean_t_chron, SD_t_chron));

        prob_ctrl.append((norm_density_ctrl[len_runner] / (norm_density_ctrl[len_runner] + (norm_density_a[len_runner]/3) + (norm_density_suba[len_runner]/3) + (norm_density_chron[len_runner]/3))));
        if prob_ctrl[len_runner] < Decimal(.000000000000000000000000000000000000001):
            prob_ctrl[len_runner] = Decimal(.000000000000000000000000000000000000001)
        
        prob_stroke.append((((norm_density_a[len_runner]/3) + (norm_density_suba[len_runner]/3) + (norm_density_chron[len_runner]/3)) / ((norm_density_ctrl[len_runner] + (norm_density_a[len_runner]/3) + (norm_density_suba[len_runner]/3) + (norm_density_chron[len_runner]/3)))));
        
        like_ratio.append(prob_stroke[len_runner]/prob_ctrl[len_runner]);
        

        prob_tw_a.append(norm_density_a[len_runner]/(norm_density_a[len_runner] + norm_density_suba[len_runner] + norm_density_chron[len_runner]));
        prob_tw_suba.append(norm_density_suba[len_runner]/(norm_density_a[len_runner] + norm_density_suba[len_runner] + norm_density_chron[len_runner]));
        prob_tw_chron.append(norm_density_chron[len_runner]/(norm_density_a[len_runner] + norm_density_suba[len_runner] + norm_density_chron[len_runner]));

        len_runner = len_runner+1

    nfl_matrix = [nfl_value, prob_stroke, like_ratio, prob_tw_a, prob_tw_suba, prob_tw_chron];

    #print(nfl_value) #get rid of this before deployment

    placement = nfl_value.index(user_nfl_input)

    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    if like_ratio[placement]<=1:
        ratio_msg = "Very low likelihood of recent stroke"
    elif 1<like_ratio[placement]<=2:
        ratio_msg = "Non-diagnostic for stroke"
    elif 2<like_ratio[placement]<=10:
        ratio_msg = "Reasonable likelihood of recent stroke, correlate with the probability of stroke time windows as below"
    else:
        ratio_msg = "Very high likelihood of recent stroke, correlate with the probability of stroke time windows as below"

    if like_ratio[placement]<1:
        like_ratio[placement] = truncate(like_ratio[placement],2)
    if like_ratio[placement]>=1:
        like_ratio[placement] = round(like_ratio[placement])

    output_nfl = [truncate((prob_stroke[placement]*100),1), truncate(round(like_ratio[placement])), truncate((prob_tw_a[placement]*100),2), truncate((prob_tw_suba[placement]*100),2), truncate((prob_tw_chron[placement]*100),2), ratio_msg]
    # Do not need past 3 decimal points. Round at send.
    #likelihood ratio = <1 - 3 decimal. if >1, then to 1 decimal point
    #
    return output_nfl