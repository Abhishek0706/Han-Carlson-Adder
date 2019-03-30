
public class HanCarlson {
    static int n=19;

    public static void main(String[] args) {
        mainprogramme();
        preprocessmodule();
        pre_processmodule();
        generatecarry();
        findsum();
        grey();
        black();
        generatecarry();
       
    }
    static void mainprogramme(){
        if(n%2!=0) n++;
        
        System.out.println("module HanCarlson(a,b,sum);"
                + "\ninput ["+(n-1)+":0] a,b;"
                + "\noutput["+(n-1)+":0] sum;"
                + "\nwire["+(n-1)+":0] carry;"
                + "\nwire["+(n-1)+":0] ppp,ppg;"
                + "\npreprocess pp(a,b,ppp,ppg);"
                + "\ngeneratecarry gc(ppp,ppg,carry);"
                + "\nfindsum fs(ppp,carry,sum);"
                + "\nendmodule\n");

        
    }
    static void generatecarry(){
        System.out.println("module generatecarry(p,g,c);");
        System.out.println("input ["+(n-1)+":0] p,g;"
                + "\noutput["+(n-1)+":0] c;");
        System.out.println("//step bk begin");
        int black =1;
        int grey =1;
        for(int i=n-1;i>2;i=i-2){
            System.out.println("black b1"+black+"(p["+i+"],g["+i+"],p["+(i-1)+"],g["+(i-1)+"],p"+i+"_"+(i-1)+",g"+i+"_"+(i-1)+");");
            black++;
        }
        System.out.println("grey g11(p[1],g[1],g[0],g1_0);\n"
                + "buf(c[1],g1_0);");
        for(int i=0;i<n;i+=2){
            System.out.println("buf(p"+i+"_"+i+",p["+i+"]);");
            System.out.println("buf(g"+i+"_"+i+",g["+i+"]);");
        }
        black =1;
        grey =1;
        int range =2;
        int step=0;
        boolean notfound =true;
        while(notfound){
            if(n>range){
                step++;
                range *=2;
            }
            else{
                notfound = false;
            }
        }
        
        //System.out.println(step);
     
        //kodge stone
        //odd
        int diff;
        for(int s=2;s<=step+1;s++){
            System.out.println("//step"+s);
            diff= (int)Math.pow(2, s-1);
            diff--;
            //System.out.println(diff);
            black =1;
            grey =1;
            
            for(int i=n-1;i>=diff;i-=2){
                if(i-diff>0){
                    if(i-diff-diff-1>0){
                        //black
                        System.out.println("black b"+s+""+black+"(p"+i+"_"+(i-diff)+","
                                + "g"+i+"_"+(i-diff)+","
                                        + "p"+(i-diff-1)+"_"+(i-diff-diff-1)+","
                                                + "g"+(i-diff-1)+"_"+(i-diff-diff-1)+","
                                                        + "p"+i+"_"+(i-diff-diff-1)+","
                                                                + "g"+i+"_"+(i-diff-diff-1)+");");
                        black++;
                    }
                    else{
                        //grey
                        System.out.println("grey g"+s+grey+"(p"+i+"_"+(i-diff)+","
                                + "g"+i+"_"+(i-diff)+","
                                        + "g"+(i-diff-1)+"_0,"
                                                 + "g"+i+"_0);");
                        System.out.println("buf(c["+i+"],g"+i+"_0);");
                        grey++;
                    }
                }
                
            }
            
            
        }
        //even
        grey =1;
        System.out.println("//step"+(step+2)+" for even");
        for(int i=2;i<n;i+=2){
             System.out.println("grey g"+(step+2)+""+grey+"(p"+i+"_"+i+",g"+i+"_"+i+",g"+(i-1)+"_0,c["+i+"]);");
             grey++;
        }
        System.out.println("buf(c[0],g0_0);");
        System.out.println("endmodule\n");
        
        
    }
    
    
    static void preprocessmodule(){
        System.out.println("module preprocess(a,b,p,g);");
        System.out.println("input ["+(n-1)+":0] a,b;"
                + "\noutput["+(n-1)+":0] p,g;");
        for(int i=0;i<n;i++){
            System.out.println("pre_process pp"+i+"(a["+i+"],b["+i+"],p["+i+"],g["+i+"]);");
            
        }
        System.out.println("endmodule\n");
    }
    static void pre_processmodule(){
        System.out.println("module pre_process(a,b,p,g);");
        System.out.println("input a,b;\noutput p,g;\n"
                + "xor(p,a,b);\nand(g,a,b);\n"
                + "endmodule\n");
    }
    static void findsum(){
        System.out.println("module findsum(a,b,c);");
        System.out.println("input ["+(n-1)+":0] a,b;"
                + "\noutput["+(n-1)+":0] c;");
        System.out.println("xor(c[0],a[0],1'b0);");
        for(int i=1;i<n;i++){
            System.out.println("xor(c["+i+"],a["+i+"],b["+(i-1)+"]);");
        }
        System.out.println("endmodule\n");
    }
    static void grey(){
        System.out.println("module grey(p1,g1,g2,g);");
        System.out.println("input p1,g1,g2;\noutput g;\n"
                + "wire w;\n"
                + "and(w,p1,g2);\n"
                + "or(g,w,g1);");
        System.out.println("endmodule\n");
    }
    static void black(){
        System.out.println("module black(p1,g1,p2,g2,p,g);");
        System.out.println("input p1,g1,p2,g2;\noutput p,g;\n"
                + "wire w;\n"
                + "and(p,p1,p2);\n"
                + "and(w,p1,g2);\n"
                + "or(g,w,g1);");
        System.out.println("endmodule\n");
    }
    
}
