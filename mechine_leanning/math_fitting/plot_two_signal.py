import numpy as np
import matplotlib.pyplot as plt


def two_signal():
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2
    nse3 = np.random.randn(len(t))  # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2
    s3 = np.sin(2 * np.pi * 10 * t) + nse3

    plt.plot(t, s1, label='s1')  # 多个图层就添加多个
    plt.plot(t, s2, label='s2')
    plt.plot(t, s3, label='s3')

    plt.xlim(0, 2)  # x轴长度
    plt.title('noise figure')  # 标题
    plt.xlabel('time')  # x轴标签
    plt.ylabel('s1 and s2')  # y轴标签
    plt.grid(True)  # 网格

    plt.legend()  # 图例，在plot中设置label
    plt.tight_layout()  # 多图自适应间隔
    plt.show()


def two_signal_sub():
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    two_signal()
