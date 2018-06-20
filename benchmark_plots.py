import pandas as pd
import matplotlib

# matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv('results.csv')
df_acc = df[df['type'] == 'accuracy']
b = [0, 0]
for i, (j, group) in enumerate(df_acc.groupby('name')):
    b[i] = group.reset_index()
feer, feerci = b
ax = plt.subplot('111')
plt.hist([feer.ci_min - feerci.ci_min, feer.ci_max - feerci.ci_max], label=['Lower Bound', 'Upper Bound'])
plt.legend()
plt.xlabel('Error')
plt.ylabel('Count')
plt.savefig('feerci_accuracy.pdf')

plt.clf()
df_speed = df[df['type'] == 'speed']
df_speed.sort_values(['name', 'size'])
sizes = sorted(df_speed['size'].unique())
name2label = {
    'bob_once': 'bob (single eer)',
    'naive_bob':'bob (naive bootstrap)',
    'sorted_bob':'bob (sorted bootstrap)',
    'sorted_feer':'feer (sorted bootstrap)',
    'feerci_on_presorted': 'feerci (unsorted)',
    'feerci_on_unsorted': 'feerci (pre-sorted)'}
colours = ['C0','C1','C5','C3','C4','C2','C6','C7']
for i,name in enumerate(['naive_bob', 'sorted_bob', 'sorted_feer','bob_once' ,'feerci_on_unsorted','feerci_on_presorted']):
    d = df_speed[df_speed.name == name].groupby('size').mean().reset_index()
    plt.plot(d['size'], d.time, label=name2label.get(name, name), linewidth=3,c=colours[i])
plt.legend()
plt.xlabel('score list size')
plt.ylabel('avg time (s)')
plt.xscale('log')
# plt.yscale('log')
plt.savefig('feerci_speed.pdf')
