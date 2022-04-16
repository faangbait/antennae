struct ATM {
    twenties: i32,
    fifties: i32,
    hundreds: i32,
    twohundreds: i32,
    fivehundreds: i32
}


/** 
 * `&self` means the method takes an immutable reference.
 * If you need a mutable reference, change it to `&mut self` instead.
 */
impl ATM {

    fn new() -> Self {
        ATM {twenties: 0, fifties: 0, hundreds: 0, twohundreds: 0, fivehundreds: 0}
    }
    
    fn deposit(&mut self, banknotes_count: Vec<i32>) {
        self.twenties += banknotes_count[0];
        self.fifties += banknotes_count[1];
        self.hundreds += banknotes_count[2];
        self.twohundreds += banknotes_count[3];
        self.fivehundreds += banknotes_count[4];
    }
    
    fn withdraw(&mut self, amount: i32) -> Vec<i32> {
        let mut remaining = amount.clone();
        let mut bills = vec![0,0,0,0,0];

        while remaining > 0 {
            if remaining >= 500 {
                let count = self.fivehundreds.min(remaining / 500);
                if count < 0 { self.deposit(bills); return vec![-1]; }
                remaining -= count * 500;
                self.fivehundreds = self.fivehundreds - count;
                bills[4] += count;

            }

            if remaining >= 200 {
                let count = self.twohundreds.min(remaining / 200);
                if count < 0 { self.deposit(bills); return vec![-1]; }
                remaining -= count * 200;
                self.twohundreds = self.twohundreds - count;
                bills[3] += count;
            }

            if remaining >= 100 {
                let count = self.hundreds.min(remaining / 100);
                if count < 0 { self.deposit(bills); return vec![-1]; }
                remaining -= count * 100;
                self.hundreds = self.hundreds - count;
                bills[2] += count;
            }
            
            if remaining >= 50 {
                let count = self.fifties.min(remaining / 50);
                if count < 0 { self.deposit(bills); return vec![-1]; }
                remaining -= count * 50;
                self.fifties = self.fifties - count;
                bills[1] += count;
            }

            if remaining >= 20 {
                let count = self.twenties.min(remaining / 20);
                if count < 0 { self.deposit(bills); return vec![-1]; }
                remaining -= count * 20;
                self.twenties = self.twenties - count;
                bills[0] += count;
            }

            if remaining > 0 {
                self.deposit(bills); return vec![-1];
            }
        }
        bills
    }
}

impl Default for ATM {
    fn default() -> Self {
        Self::new()
    }
}

/**
 * Your ATM object will be instantiated and called as such:
 * let obj = ATM::new();
 * obj.deposit(banknotesCount);
 * let ret_2: Vec<i32> = obj.withdraw(amount);
 */

 pub fn main() {
    // let mut obj = ATM::new();
    // obj.deposit(vec![0,0,1,2,1]);
    // let ret_2: Vec<i32> = obj.withdraw(600);
    // obj.deposit(vec![0,1,0,1,1]);
    // let ret_2 = obj.withdraw(600);
    // assert_eq!(ret_2, vec![-1]);
    // let ret_2 = obj.withdraw(550);
    // assert_eq!(ret_2, vec![0,1,0,0,1]);
    
    let mut obj = ATM::new();
    obj.deposit(vec![0,10,0,3,0]);
    let ret_2: Vec<i32> = obj.withdraw(500);
    assert_eq!(ret_2, vec![0,2,0,2,0]);

    let mut obj = ATM::new();
    obj.deposit(vec![0,0,1,2,2]);
    obj.withdraw(600);
    obj.deposit(vec![0,1,0,1,1]);
    
 }
