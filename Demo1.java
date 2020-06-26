interface T1{
	public void f1();
}

class c1 implements T1{
	public void f1(){
		System.out.println("Hi");
	}
}

class Demo1{
	public static void main(String args[]){
		c1 c = new c1();
		c.f1();

		T1 d = () -> {System.out.println("Bye")};
		d.f1(); 
	}
}