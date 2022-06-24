
pub struct Solution {}

impl Solution {
    /// Given a string s, return the longest palindromic substring in s.
    pub fn longest_palindrome(s: String) -> String {
        let n = s.len();
        if n < 2 {
            return s;
        }

        let s_arr = s.as_bytes();


        let mut table = vec![vec![false; n];n];

        for i in 0..n {
            table[i][i] = true;
        }
        
        let mut max_len = 1;
        let mut start = 0;

        for i in 0..n-1 {
            if s_arr[i] == s_arr[i+1] {
                table[i][i+1] = true;
                start = i;
                max_len = 2;
            }
        }

        for k in 3..=n {
            for i in 0..=n-k {
                let j = i + k - 1;
                if s_arr[i] == s_arr[j] && table[i+1][j-1] {
                    table[i][j] = true;
                    if k > max_len {
                        start = i;
                        max_len = k;
                    }
                }
            }
        }
        s[start..start+max_len].to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn geeks() {
        assert_eq!(Solution::longest_palindrome("forgeeksskeegfor".to_string()), "geeksskeeg".to_string());
    }
    #[test]
    pub fn simple() {
        assert_eq!(Solution::longest_palindrome("aba".to_string()), "aba".to_string());
    }

    #[test]
    pub fn wholeword() {
        assert_eq!(Solution::longest_palindrome("racecar".to_string()), "racecar".to_string());
    }

    #[test]
    pub fn off_center() {
        assert_eq!(Solution::longest_palindrome("babcd".to_string()), "bab".to_string());
    }
    
    #[test]
    pub fn doubled_chars() {
        assert_eq!(Solution::longest_palindrome("cbbd".to_string()), "bb".to_string());
    }

    #[test]
    pub fn multiple_same_sized() {
        assert_eq!(Solution::longest_palindrome("boblolfoo".to_string()), "bob".to_string());
    }

    #[test]
    pub fn single_char() {
        assert_eq!(Solution::longest_palindrome("a".to_string()), "a".to_string());
    }

    #[test]
    pub fn long_one() {
        assert_eq!(Solution::longest_palindrome("civilwartestingwhetherthatnaptionoranynartionsoconceivedandsodedicatedcanlongendureWeareqmetonagreatbattlefiemldoftzhatwarWehavecometodedicpateaportionofthatfieldasafinalrestingplaceforthosewhoheregavetheirlivesthatthatnationmightliveItisaltogetherfangandproperthatweshoulddothisButinalargersensewecannotdedicatewecannotconsecratewecannothallowthisgroundThebravelmenlivinganddeadwhostruggledherehaveconsecrateditfaraboveourpoorponwertoaddordetractTgheworldadswfilllittlenotlenorlongrememberwhatwesayherebutitcanneverforgetwhattheydidhereItisforusthelivingrathertobededicatedheretotheulnfinishedworkwhichtheywhofoughtherehavethusfarsonoblyadvancedItisratherforustobeherededicatedtothegreattdafskremainingbeforeusthatfromthesehonoreddeadwetakeincreaseddevotiontothatcauseforwhichtheygavethelastpfullmeasureofdevotionthatweherehighlyresolvethatthesedeadshallnothavediedinvainthatthisnationunsderGodshallhaveanewbirthoffreedomandthatgovernmentofthepeoplebythepeopleforthepeopleshallnotperishfromtheearth".to_string()), "ranynar".to_string());
    }

    #[test]
    pub fn even_longer() {
        assert_eq!(Solution::longest_palindrome("zudfweormatjycujjirzjpyrmaxurectxrtqedmmgergwdvjmjtstdhcihacqnothgttgqfywcpgnuvwglvfiuxteopoyizgehkwuvvkqxbnufkcbodlhdmbqyghkojrgokpwdhtdrwmvdegwycecrgjvuexlguayzcammupgeskrvpthrmwqaqsdcgycdupykppiyhwzwcplivjnnvwhqkkxildtyjltklcokcrgqnnwzzeuqioyahqpuskkpbxhvzvqyhlegmoviogzwuiqahiouhnecjwysmtarjjdjqdrkljawzasriouuiqkcwwqsxifbndjmyprdozhwaoibpqrthpcjphgsfbeqrqqoqiqqdicvybzxhklehzzapbvcyleljawowluqgxxwlrymzojshlwkmzwpixgfjljkmwdtjeabgyrpbqyyykmoaqdambpkyyvukalbrzoyoufjqeftniddsfqnilxlplselqatdgjziphvrbokofvuerpsvqmzakbyzxtxvyanvjpfyvyiivqusfrsufjanmfibgrkwtiuoykiavpbqeyfsuteuxxjiyxvlvgmehycdvxdorpepmsinvmyzeqeiikajopqedyopirmhymozernxzaueljjrhcsofwyddkpnvcvzixdjknikyhzmstvbducjcoyoeoaqruuewclzqqqxzpgykrkygxnmlsrjudoaejxkipkgmcoqtxhelvsizgdwdyjwuumazxfstoaxeqqxoqezakdqjwpkrbldpcbbxexquqrznavcrprnydufsidakvrpuzgfisdxreldbqfizngtrilnbqboxwmwienlkmmiuifrvytukcqcpeqdwwucymgvyrektsnfijdcdoawbcwkkjkqwzffnuqituihjaklvthulmcjrhqcyzvekzqlxgddjoir".to_string()), "gykrkyg".to_string());
    }

}

fn main() {}
