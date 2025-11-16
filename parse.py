from bs4 import BeautifulSoup
import json


def extract_comment_text(comment_div):
    """
    Extract text from a comment div.
    
    Args:
        comment_div: BeautifulSoup div element with class 'nujij__comment'
        
    Returns:
        Comment text as string
    """
    body_div = comment_div.find('div', class_='nujij__comment-body')
    if body_div:
        return body_div.get_text(separator='\n', strip=True)
    return ''


def parse_comment_with_replies(wrapper):
    """
    Parse a comment and its replies recursively.
    
    Args:
        wrapper: BeautifulSoup div element with class 'nujij__comment-wrapper'
        
    Returns:
        Dictionary with 'text' and 'replies' keys
    """
    comment_div = wrapper.find('div', class_='nujij__comment', recursive=False)
    if not comment_div:
        return None
    
    # Extract comment text
    comment_text = extract_comment_text(comment_div)
    
    # Initialize comment dictionary
    comment_data = {
        'text': comment_text,
        'replies': []
    }
    
    # Find replies section
    replies_div = wrapper.find('div', class_='nujij__replies', recursive=False)
    if replies_div:
        # Find all direct child comment wrappers (replies)
        reply_wrappers = replies_div.find_all('div', class_='nujij__comment-wrapper', recursive=False)
        for reply_wrapper in reply_wrappers:
            reply_data = parse_comment_with_replies(reply_wrapper)
            if reply_data:
                comment_data['replies'].append(reply_data)
    
    return comment_data


def parse_comments(html_file):
    """
    Parse comments from HTML file and return as list of dictionaries.
    
    Args:
        html_file: Path to HTML file containing comments
        
    Returns:
        List of comment dictionaries with text and replies
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    comments = []
    
    # Find all top-level comment wrappers
    # We need to find comment wrappers that are NOT inside a replies div
    all_wrappers = soup.find_all('div', class_='nujij__comment-wrapper')
    
    for wrapper in all_wrappers:
        # Check if this wrapper is a top-level comment (not a reply)
        # A reply has 'nujij__comment--reply' class in its comment div
        comment_div = wrapper.find('div', class_='nujij__comment', recursive=False)
        if comment_div and 'nujij__comment--reply' not in comment_div.get('class', []):
            comment_data = parse_comment_with_replies(wrapper)
            if comment_data:
                comments.append(comment_data)
    
    return comments


def main():
    """Main function to parse comments and save as JSON."""
    input_file = 't.txt'
    output_file = 'comments.json'
    
    print(f"Reading comments from {input_file}...")
    comments = parse_comments(input_file)
    
    print(f"Found {len(comments)} comments")
    
    # Save to JSON with pretty formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    
    print(f"Comments saved to {output_file}")
    
    # Print summary
    print("\nSummary:")
    for i, comment in enumerate(comments, 1):
        reply_count = len(comment['replies'])
        text_preview = comment['text'][:60]
        if reply_count > 0:
            print(f"{i}. {text_preview}... ({reply_count} replies)")
        else:
            print(f"{i}. {text_preview}...")


if __name__ == '__main__':
    main()
