__author__ = 'root'
import re

def naive_string_matching(pattern, text): #O(n(m-n+1))
    lpattern = len(pattern)
    ltext = len(text)
    result = []
    if lpattern <= ltext:
        for i in range(0, (ltext - lpattern)+1):
            if pattern[0] == text[i]:
                k = i
                for j in range(1, lpattern):
                    k += 1
                    if pattern[j] != text[k]:
                        break
                    elif j == lpattern - 1:
                        result.append(i)

    return result

def naive_string_matching_different_character_in_pattern(pattern, text):#O(n)
    lpattern = len(pattern)
    ltext = len(text)
    result = []
    if lpattern <= ltext:
        for i in range(0, (ltext - lpattern)+1):
            if pattern[0] == text[i]:
                k = i
                for j in range(1, lpattern):
                    k += 1
                    if pattern[j] != text[k]:
                        i += lpattern -1
                        break
                    elif j == lpattern - 1:
                        result.append(i)

    return result

def naive_string_matching_gap_character_in_pattern(pattern, text):#O()
    lpattern = len(pattern)
    ltext = len(text)
    result = []
    if lpattern <= ltext:
        for i in range(0, (ltext - lpattern)+1):
            if pattern[0] == text[i]:
                k = i
                for j in range(1, lpattern):
                    k += 1
                    if pattern[j] != text[k]:
                        i += lpattern -1
                        break
                    elif j == lpattern - 1:
                        result.append(i)

    return result

def clear_doble_string(STDIN):
    result = ''
    for i in range(0, len(STDIN)):
        result += STDIN[i]
        result = result if len(result) == 1 or result[-2] != result[-1] else result[0:len(result)-2]
    STDOUT = result
    return STDOUT if len(STDOUT) > 0 else 'Empty String'

def get_all_two_character_posible(s):
    list = {}
    for i in range(0, len(s)-1):
        for j in range(i+1, len(s)):
            if s[i] != s[j]:
                string_aux = s[i] + s[j]
                if not((s[i] + s[j]) in list) and not((s[j] + s[i]) in list):
                    list[string_aux] = 1
    return list.keys()

def two_character_make_t(s,l1,l2):
    result = ''
    for i in range(0, len(s)):
        result += s[i] if s[i] == l1 or s[i] == l2 else ''
    return result

def two_character_is_valid(t):
    if len(t) <= 1:
        return True
    x1 = t[0]
    x2 = t[1]
    for i in range(0, len(t)-1):
        if t[i] == t[i+1] or (t[i] != x1 and t[i] != x2):
            return False
    return t[-1] == x1 or t[-1] == x2

def circular_string(s, l, k):
    result = ''
    for i in range(0, len(s)):
        if s[i] == l:
            r = i+k
            index = r % len(s)
            result = s[r] if r < len(s) else s[index]
            break
    return result

def find_noise(s):
    result = 0
    sms = 'SOS'
    for i in range(0, len(s)):
        r = i % 3
        if s[i] != sms[r]:
            result += 1
    return result

def exist_word(s):
    word = 'hackerrank'
    index = 0
    count = 0
    for i in range(0, len(word)):
        for j in range(index, len(s)):
            if word[i] == s[j]:
                index = j+1
                count += 1
                break
    return 'YES' if count == len(word) else 'NO'

if __name__ == "__main__":
    print exist_word('hackerworld')


##### Est es la manera de entrada de los valores ####
#   import sys
#   s_len = int(raw_input().strip())
#   s = raw_input().strip()
