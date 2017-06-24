


from matplotlib.ticker import MultipleLocator
import os
run olg3pernol

# First let us initialize some arguments
args = (0.96, 3,1, 0.35, 0.05)
n = np.array([1,1,0.2])
model = olg3pernol(n,args)
print(model)

#Now we want to compute steady state.
b_init = np.array([0.1,0.5])
model.ss(b_init)

#What happens when we change beta?
bnew = 0.55 ** (1/20)
argnew = (bnew, 3, 1, 0.35, 0.05)
model2 = olg3pernol(n,argnew)
print(model2)
model2.ss(b_init)

#Simulating a perturbation
perturbation = np.array([0.8,1.1])
pb = perturbation * model.bss
transitionpath = model.perturb(pb, chi=0.01, T = 50)

plot = True

if plot:
    '''
    --------------------------------------------------------------------
    cur_path    = string, path name of current directory
    output_fldr = string, folder in current path to save files
    output_dir  = string, total path of images folder
    output_path = string, path of file name of figure to be saved
    xx          = (45,) vector, values of xx
    yy          = (45,) vector, values of yy
    --------------------------------------------------------------------
    '''
    # Create directory if images directory does not already exist
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    output_fldr = 'images'
    output_dir = os.path.join(cur_path, output_fldr)
    if not os.access(output_dir, os.F_OK):
        os.makedirs(output_dir)

    # Plot line plot of xx and yy
    plt.plot(transitionpath.sum(axis=1)))
    # for the minor ticks, use no labels; default NullFormatter
    minorLocator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.grid(b=True, which='major', color='0.65', linestyle='-')
    plt.title('Transition Path of Capital', fontsize=20)
    plt.xlabel('Time')
    plt.ylabel('Capital')
    output_path = os.path.join(output_dir, 'Ktransition')
    plt.savefig(output_path)
    # plt.show()
    plt.close()
