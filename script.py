import tkinter as tk
from tkinter import ttk
import random
win = tk.Tk()
win.resizable(width=0, height=0)
win.title("Han Carlson n-bit Adder")
n_label = ttk.Label(win, text="Enter the n:")
n_label.grid(row=0, column=0, sticky=tk.W)
n_value = tk.IntVar()
n_value.set(16)
n_entrybox = ttk.Entry(win, width=14, textvariable=n_value)
n_entrybox.grid(row=0, column=1)
random_n_label = ttk.Label(win, text="Number of test values:")
random_n_label.grid(row=1, column=0, sticky=tk.W)
random_n_value = tk.IntVar()
random_n_value.set(10)
random_n_entrybox = ttk.Entry(win, width=14, textvariable=random_n_value)
random_n_entrybox.grid(row=1, column=1)
random_range_label = ttk.Label(win, text="Range of test values:")
random_range_label.grid(row=2, column=0, sticky=tk.W)
random_range_value = tk.IntVar()
random_range_value.set(int(2**(n_value.get()-2)))
random_range_entrybox = ttk.Entry(
    win, width=14, textvariable=random_range_value)
random_range_entrybox.grid(row=2, column=1)
def main():
    n = n_value.get()
    random_n = random_n_value.get()
    random_range = random_range_value.get()
    l = []
    l.append(f"module adder_{n}(a,b,s);")
    l.append(f"input [{n-1}:0] a,b;")
    l.append(f"output [{n-1}:0] s;")
    l.append(f"wire [{n-1}:0] p,g,c;")
    for i in range(n):
        l.append(f"pre_process pp{i}(a[{i}],b[{i}],p[{i}],g[{i}]);")
    l.append(f"han_carlson c_gen(p,g,c);")
    l.append(f"buf (s[0],p[0]);")
    for i in range(1, n):
        l.append(f"xor (s[{i}],p[{i}],c[{i-1}]);")
    l.append(f"endmodule\n")
    l.append(f"module han_carlson(p,g,c);")
    l.append(f"input [{n-1}:0] p,g;")
    l.append(f"output [{n-1}:0] c;")
    l.append("//step bk begin")
    black, grey = 1, 1
    for i in range(n-1, 2, -2):
        l.append("black b1"+str(black)+"(p["+str(i)+"],g["+str(i)+"],p["+str(
            i-1)+"],g["+str(i-1)+"],p"+str(i)+"_"+str(i-1)+",g"+str(i)+"_"+str(i-1)+");")
        black += 1
    l.append("grey g11(p[1],g[1],g[0],g1_0);\n"
             + "buf(c[1],g1_0);")
    for i in range(0, n, 2):
        l.append("buf(p"+str(i)+"_"+str(i)+",p["+str(i)+"]);")
        l.append("buf(g"+str(i)+"_"+str(i)+",g["+str(i)+"]);")
    black, grey = 1, 1
    range_, step = 2, 0
    notfound = True
    while notfound:
        if n > range_:
            step += 1
            range_ *= 2
        else:
            notfound = False
    for s in range(2, step+2):
        l.append(f"//step {s}")
        diff = int(2**(s-1))
        diff -= 1
        black, grey = 1, 1
        for i in range(n-1, diff-1, -2):
            if i-diff > 0:
                if i-2*diff-1 > 0:
                    l.append("black b"+str(s)+""+str(black)+"(p"+str(i)+"_"+str(i-diff)+","
                             + "g"+str(i)+"_"+str(i-diff)+","
                             + "p"+str(i-diff-1)+"_"+str(i-diff-diff-1)+","
                                                + "g"+str(i-diff-1)+"_" +
                             str(i-diff-diff-1)+","
                             + "p"+str(i)+"_"+str(i-diff-diff-1)+","
                             + "g"+str(i)+"_"+str(i-diff-diff-1)+");")
                    black += 1

                else:
                    l.append("grey g"+str(s)+str(grey)+"(p"+str(i)+"_"+str(i-diff)+","
                             + "g"+str(i)+"_"+str(i-diff)+","
                             + "g"+str(i-diff-1)+"_0,"
                             + "g"+str(i)+"_0);")
                    l.append("buf(c["+str(i)+"],g"+str(i)+"_0);")
                    grey += 1

    grey = 1
    l.append("//step"+str(step+2)+" for even")
    for i in range(2, n, 2):
        l.append("grey g"+str(step+2)+""+str(grey)+"(p"+str(i)+"_" +
                 str(i)+",g"+str(i)+"_"+str(i)+",g"+str(i-1)+"_0,c["+str(i)+"]);")
        grey += 1
    l.append("buf(c[0],g0_0);")
    l.append(f"endmodule\n")
    l.append(
        "module pre_process(a,b,p,g);\ninput a,b;\noutput p,g;\nxor (p,a,b);\nand (g,a,b);\nendmodule\n")
    l.append("module grey(p1,g1,g2,g);\ninput p1,g1,g2;\noutput g;\nwire w;\nand (w,p1,g2);\nor (g,g1,w);\nendmodule\n")
    l.append("module black(p1,g1,p2,g2,p,g);\ninput p1,g1,p2,g2;\noutput p,g;\nwire w;\nand (p,p1,p2);\nand (w,p1,g2);\nor (g,w,g1);\nendmodule\n")
    s = "\n".join(l)
    print(f"The generated {n}-bit Han Carlson Adder")
    print(s)
    text_file = open("main.v", "w+")
    text_file.write(s)
    text_file.close()
    l_test = []
    l_test.append(f"`timescale 1ps / 1ps")
    l_test.append(f"module simu();")
    l_test.append(f"    reg [{n-1}:0] a,b;")
    l_test.append(f"    wire [{n-1}:0] s;")
    l_test.append(f"    adder_{n} n1(.a(a),.b(b),.s(s));")
    l_test.append(f"    initial begin")
    l_test.append(f"    $monitor(a,b,s);")
    for i in range(int(random_n)):
        l_test.append(
            f"    #2 a={random.randint(a=0,b=random_range)};")
        l_test.append(
            f"     b={random.randint(a=0,b=random_range)};")
    l_test.append(f"    #2 $finish;")
    l_test.append(f"    end")
    l_test.append(f"endmodule")
    s_test = "\n".join(l_test)
    print("The generated test bench")
    print(s_test)
    text_file = open("test_bench.v", "w+")
    text_file.write(s_test)
    text_file.close()
submit_button = tk.Button(
    win, text="Generate", command=main)
submit_button.grid(row=3,columnspan=3)
win.mainloop()
