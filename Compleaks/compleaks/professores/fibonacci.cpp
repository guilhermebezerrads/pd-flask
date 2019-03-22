#include <stdio>
using namespace std;

int fibonacci(int n){
	if (n<1){
		return n; 
	}else{
		return fibonacci(n-1) + fibonacci(n-2);
	}
}

int main(){

	int a;
	cout << "Entre com um número de fibonacci:" << endl;
	cin >> a;

	cout << fibonacci(a); 

	return 0;
}