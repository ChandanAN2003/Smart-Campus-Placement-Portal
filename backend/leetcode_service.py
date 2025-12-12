import requests
import random

LEETCODE_URL = "https://leetcode.com/graphql"

TAG_MAPPING = {
    "Arrays": "array",
    "Strings": "string",
    "LinkedList": "linked-list",
    "StackQueue": "stack",
    "Trees": "tree",
    "DP": "dynamic-programming",
    "Graphs": "graph"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com/'
}

# --- Fallback Data ---

# --- Fallback Data (Expanded) ---

FALLBACK_PROBLEMS = {
    "Arrays": [
        {"id": "1", "title": "Two Sum", "titleSlug": "two-sum", "difficulty": "Easy"},
        {"id": "26", "title": "Remove Duplicates from Sorted Array", "titleSlug": "remove-duplicates-from-sorted-array", "difficulty": "Easy"},
        {"id": "27", "title": "Remove Element", "titleSlug": "remove-element", "difficulty": "Easy"},
        {"id": "35", "title": "Search Insert Position", "titleSlug": "search-insert-position", "difficulty": "Easy"},
        {"id": "66", "title": "Plus One", "titleSlug": "plus-one", "difficulty": "Easy"},
        {"id": "88", "title": "Merge Sorted Array", "titleSlug": "merge-sorted-array", "difficulty": "Easy"},
        {"id": "118", "title": "Pascal's Triangle", "titleSlug": "pascals-triangle", "difficulty": "Easy"},
        {"id": "121", "title": "Best Time to Buy and Sell Stock", "titleSlug": "best-time-to-buy-and-sell-stock", "difficulty": "Easy"},
        {"id": "136", "title": "Single Number", "titleSlug": "single-number", "difficulty": "Easy"},
        {"id": "169", "title": "Majority Element", "titleSlug": "majority-element", "difficulty": "Easy"},
        
        {"id": "11", "title": "Container With Most Water", "titleSlug": "container-with-most-water", "difficulty": "Medium"},
        {"id": "15", "title": "3Sum", "titleSlug": "3sum", "difficulty": "Medium"},
        {"id": "16", "title": "3Sum Closest", "titleSlug": "3sum-closest", "difficulty": "Medium"},
        {"id": "18", "title": "4Sum", "titleSlug": "4sum", "difficulty": "Medium"},
        {"id": "31", "title": "Next Permutation", "titleSlug": "next-permutation", "difficulty": "Medium"},
        {"id": "33", "title": "Search in Rotated Sorted Array", "titleSlug": "search-in-rotated-sorted-array", "difficulty": "Medium"},
        {"id": "34", "title": "Find First and Last Position of Element in Sorted Array", "titleSlug": "find-first-and-last-position-of-element-in-sorted-array", "difficulty": "Medium"},
        {"id": "53", "title": "Maximum Subarray", "titleSlug": "maximum-subarray", "difficulty": "Medium"},
        {"id": "56", "title": "Merge Intervals", "titleSlug": "merge-intervals", "difficulty": "Medium"},
        
        {"id": "4", "title": "Median of Two Sorted Arrays", "titleSlug": "median-of-two-sorted-arrays", "difficulty": "Hard"},
        {"id": "41", "title": "First Missing Positive", "titleSlug": "first-missing-positive", "difficulty": "Hard"},
        {"id": "42", "title": "Trapping Rain Water", "titleSlug": "trapping-rain-water", "difficulty": "Hard"}
    ],
    "Strings": [
        {"id": "13", "title": "Roman to Integer", "titleSlug": "roman-to-integer", "difficulty": "Easy"},
        {"id": "14", "title": "Longest Common Prefix", "titleSlug": "longest-common-prefix", "difficulty": "Easy"},
        {"id": "20", "title": "Valid Parentheses", "titleSlug": "valid-parentheses", "difficulty": "Easy"},
        {"id": "28", "title": "Find the Index of the First Occurrence in a String", "titleSlug": "find-the-index-of-the-first-occurrence-in-a-string", "difficulty": "Easy"},
        {"id": "58", "title": "Length of Last Word", "titleSlug": "length-of-last-word", "difficulty": "Easy"},
        {"id": "125", "title": "Valid Palindrome", "titleSlug": "valid-palindrome", "difficulty": "Easy"},
        {"id": "242", "title": "Valid Anagram", "titleSlug": "valid-anagram", "difficulty": "Easy"},
        
        {"id": "3", "title": "Longest Substring Without Repeating Characters", "titleSlug": "longest-substring-without-repeating-characters", "difficulty": "Medium"},
        {"id": "5", "title": "Longest Palindromic Substring", "titleSlug": "longest-palindromic-substring", "difficulty": "Medium"},
        {"id": "6", "title": "Zigzag Conversion", "titleSlug": "zigzag-conversion", "difficulty": "Medium"},
        {"id": "17", "title": "Letter Combinations of a Phone Number", "titleSlug": "letter-combinations-of-a-phone-number", "difficulty": "Medium"},
        
        {"id": "10", "title": "Regular Expression Matching", "titleSlug": "regular-expression-matching", "difficulty": "Hard"},
        {"id": "76", "title": "Minimum Window Substring", "titleSlug": "minimum-window-substring", "difficulty": "Hard"}
    ],
    # Kept other categories compact for brevity but enabled generally
    "LinkedList": [
        {"id": "21", "title": "Merge Two Sorted Lists", "titleSlug": "merge-two-sorted-lists", "difficulty": "Easy"},
        {"id": "83", "title": "Remove Duplicates from Sorted List", "titleSlug": "remove-duplicates-from-sorted-list", "difficulty": "Easy"},
        {"id": "141", "title": "Linked List Cycle", "titleSlug": "linked-list-cycle", "difficulty": "Easy"},
        {"id": "160", "title": "Intersection of Two Linked Lists", "titleSlug": "intersection-of-two-linked-lists", "difficulty": "Easy"},
        {"id": "203", "title": "Remove Linked List Elements", "titleSlug": "remove-linked-list-elements", "difficulty": "Easy"},
        {"id": "206", "title": "Reverse Linked List", "titleSlug": "reverse-linked-list", "difficulty": "Easy"},
        {"id": "234", "title": "Palindrome Linked List", "titleSlug": "palindrome-linked-list", "difficulty": "Easy"},
        
        {"id": "2", "title": "Add Two Numbers", "titleSlug": "add-two-numbers", "difficulty": "Medium"},
        {"id": "19", "title": "Remove Nth Node From End of List", "titleSlug": "remove-nth-node-from-end-of-list", "difficulty": "Medium"},
        
        {"id": "23", "title": "Merge k Sorted Lists", "titleSlug": "merge-k-sorted-lists", "difficulty": "Hard"}
    ]
}

# Store details for key problems to allow full functionality offline/fallback
FALLBACK_DETAILS = {
    "two-sum": {
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>",
        "examples": "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
        "test_cases": "nums = [2,7,11,15], target = 9",
        "starter_code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        "
    },
    "plus-one": {
        "title": "Plus One",
        "difficulty": "Easy",
        "description": "<p>You are given a <strong>large integer</strong> represented as an integer array <code>digits</code>, where each <code>digits[i]</code> is the <code>i<sup>th</sup></code> digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading <code>0</code>'s.</p><p>Increment the large integer by one and return <em>the resulting array of digits</em>.</p>",
        "examples": "Input: digits = [1,2,3]\nOutput: [1,2,4]\nExplanation: The array represents the integer 123.\nIncrementing by one gives 123 + 1 = 124.\nThus, the result should be [1,2,4].",
        "test_cases": "digits = [1,2,3]",
        "starter_code": "class Solution:\n    def plusOne(self, digits: List[int]) -> List[int]:\n        "
    },
    "valid-parentheses": {
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "description": "<p>Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.</p>",
        "examples": "Input: s = \"()[]{}\"\nOutput: true",
        "test_cases": "s = \"()[]{}\"",
        "starter_code": "class Solution:\n    def isValid(self, s: str) -> bool:\n        "
    },
    "climbing-stairs": {
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "description": "<p>You are climbing a staircase. It takes <code>n</code> steps to reach the top. Each time you can either climb <code>1</code> or <code>2</code> steps. In how many distinct ways can you climb to the top?</p>",
        "examples": "Input: n = 2\nOutput: 2",
        "test_cases": "n = 2",
        "starter_code": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        "
    },
     "reverse-linked-list": {
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "description": "<p>Given the <code>head</code> of a singly linked list, reverse the list, and return <em>the reversed list</em>.</p>",
        "examples": "Input: head = [1,2,3,4,5]\nOutput: [5,4,3,2,1]",
        "test_cases": "head = [1,2,3,4,5]",
        "starter_code": "class Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        "
    }
}

# Generic fallback template for problems not explicitly detailed
GENERIC_FALLBACK = {
    "title": "Problem Description",
    "difficulty": "Medium",
    "description": "<p><strong>Note:</strong> detailed description could not be loaded from LeetCode API. Please refer to LeetCode website for full details or try again later.</p>",
    "examples": "No examples available offline.",
    "test_cases": "",
    "starter_code": "class Solution:\n    def solve(self):\n        pass"
}

def get_leetcode_problem_list(topic, difficulty):
    """
    Fetches a list of problems from LeetCode using the robust problemsetQuestionList query.
    Allows fetching a large number of problems (limit 500).
    """
    tag_slug = TAG_MAPPING.get(topic, "array")
    
    # GraphQL query for the main problem set list
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
                frontendQuestionId: questionFrontendId
                title
                titleSlug
                difficulty
                topicTags {
                    slug
                }
            }
        }
    }
    """
    
    difficulty_upper = difficulty.upper()
    
    variables = {
        "categorySlug": "algorithms", # Fixed: explicitly set category
        "skip": 0,
        "limit": 100, # Realistic limit per page
        "filters": {
            "tags": [tag_slug],
            "difficulty": difficulty_upper
        }
    }
    
    try:
        # Add Origin/Referer to mimic browser better
        headers = HEADERS.copy()
        headers['Origin'] = 'https://leetcode.com'
        headers['Referer'] = 'https://leetcode.com/problemset/all/'
        
        response = requests.post(LEETCODE_URL, json={
            'query': query, 
            'variables': variables
        }, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']['problemsetQuestionList']:
                questions = data['data']['problemsetQuestionList']['questions']
                
                # Format for frontend
                result = []
                for q in questions:
                    result.append({
                        "id": q['frontendQuestionId'],
                        "title": q['title'],
                        "slug": q['titleSlug'],
                        "difficulty": q['difficulty']
                    })
                
                if result:
                    print(f"[INFO] Fetched {len(result)} problems via API")
                    return result
                    
    except Exception as e:
        print(f"LC List Error (using fallback): {e}")

    # Fallback usage
    print(f"[INFO] Using fallback for {topic} - {difficulty}")
    
    # Check if category exists in fallback
    if topic in FALLBACK_PROBLEMS:
        # Strict filtering
        problems = [p for p in FALLBACK_PROBLEMS[topic] if p['difficulty'] == difficulty]
        
        # If strict filtering returns too few problems (less than 3), 
        # append ALL fallback problems for that topic (ignoring difficulty) to show SOMETHING.
        if len(problems) < 3:
             problems = FALLBACK_PROBLEMS[topic]
             
        return problems
    
    # Last resort: return generic array problems if topic not found
    return FALLBACK_PROBLEMS.get("Arrays", [])

def get_problem_details(title_slug):
    query_details = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            content
            difficulty
            exampleTestcases
            codeSnippets {
                lang
                langSlug
                code
            }
        }
    }
    """
    
    try:
        response = requests.post(LEETCODE_URL, json={
            'query': query_details, 
            'variables': {'titleSlug': title_slug}
        }, headers=HEADERS, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']['question']:
                q = data['data']['question']
                
                # Parse snippet for Python
                starter_code = ""
                if q.get('codeSnippets'):
                    for snippet in q['codeSnippets']:
                        if snippet['langSlug'] == 'python3':
                            starter_code = snippet['code']
                            break
                            
                return {
                    "title": q['title'],
                    "difficulty": q['difficulty'],
                    "description": q['content'], # HTML content
                    "examples": q['exampleTestcases'], # Raw string of inputs
                    "test_cases": q['exampleTestcases'],
                    "constraints": [], 
                    "starter_code": starter_code,
                    "source": "LeetCode"
                }
    except Exception as e:
        print(f"LC Details Error (using fallback): {e}")

    # Fallback details
    if title_slug in FALLBACK_DETAILS:
        return FALLBACK_DETAILS[title_slug]
    
    # Generic fallback if specific details missing
    # We try to at least return the title from the slug
    generic = GENERIC_FALLBACK.copy()
    generic['title'] = title_slug.replace('-', ' ').title()
    return generic
