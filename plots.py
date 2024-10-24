import math
import matplotlib.pyplot as plt


# returns amount of bits loss, given amount of bases lost, which is based on information density
def bits_lost(bases_lost, information_density):
    return bases_lost*information_density


# returns number of bases required or sequence length given data size in bytes and information density
def bases_required(bytes, information_density):
    return math.ceil((bytes*8)/information_density)


# plots bits per bases lost
def plot_bits_bases_loss():
    # methods to plot
    methods = [('erlich', 1.55), ('grass', 1.16) ,('this work', 24), ('bornholt', 0.85) ]
    size = 1000    # 1000 bytes

    # contains data points for each method
    data_points = []    # data_points = [ (xs, ys, sequence_length, method_name), (.., .., ..)]
    for (m_name, m_density) in methods:
        xs = []
        ys = []

        seq_len = bases_required(size, m_density)

        # generate data points
        for i in range(1, seq_len+1):
            xs.append(i)
            ys.append(bits_lost(i, m_density))

        data_points.append((xs, ys, seq_len, m_name))

    # plotting
    plt.figure(figsize=(10, 6))
    bases_xticks = []
    for (xs, ys, seq_len, m_name) in data_points:
        # plt.plot(xs, ys, marker='o', linestyle='-', label=m_name)
        plt.fill_between(xs, ys, label=m_name)
        bases_xticks.append(seq_len)

    # adding titles and labels
    plt.title('Comparison of Two Datasets with Different Lengths')
    plt.xlabel('Bases Lost')
    plt.ylabel('Bits Lost')
    plt.legend()
    plt.grid()

    plt.xticks(bases_xticks)

    plt.show()


plot_bits_bases_loss()
