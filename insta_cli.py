#!/usr/bin/env python3
"""
Instagram Content Downloader CLI
Downloads all posts and reels from public Instagram profiles
"""

import instaloader
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description='Instagram Content Downloader - Download posts and reels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python insta_cli.py username                    # Download to 'downloads' folder
  python insta_cli.py username -o my_folder       # Download to custom folder
  python insta_cli.py username --limit 50         # Download only first 50 posts
  python insta_cli.py username --quiet            # Minimal output
        '''
    )
    
    parser.add_argument('username', help='Instagram username (without @)')
    parser.add_argument('-o', '--output', default='downloads', 
                       help='Output folder (default: downloads)')
    parser.add_argument('--limit', type=int, 
                       help='Limit number of posts to download')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode - minimal output')
    
    args = parser.parse_args()
    
    # Create output folder
    Path(args.output).mkdir(exist_ok=True)
    
    # Setup instaloader
    loader = instaloader.Instaloader(
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,  # No JSON files
        post_metadata_txt_pattern="",  # No .txt files
        storyitem_metadata_txt_pattern="",  # No story .txt files
        compress_json=False,
        dirname_pattern=args.output + "/{profile}",
        quiet=args.quiet
    )
    
    try:
        if not args.quiet:
            print(f"📥 Downloading content from @{args.username}")
        
        profile = instaloader.Profile.from_username(loader.context, args.username)
        
        if not args.quiet:
            print(f"👤 {profile.full_name}")
            print(f"📊 {profile.mediacount} posts total")
            if args.limit:
                print(f"🎯 Downloading first {args.limit} posts")
            print()
        
        post_count = 0
        for post in profile.get_posts():
            if args.limit and post_count >= args.limit:
                break
                
            try:
                if not args.quiet:
                    print(f"⬇️  Post {post_count + 1}: {post.shortcode}")
                loader.download_post(post, target=args.username)
                post_count += 1
                
            except Exception as e:
                if not args.quiet:
                    print(f"❌ Error downloading {post.shortcode}: {str(e)}")
                continue
        
        print(f"✅ Downloaded {post_count} posts to {args.output}/{args.username}/")
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"❌ Profile @{args.username} does not exist!")
        sys.exit(1)
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print(f"❌ Profile @{args.username} is private! You need to follow them first.")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n⏹️  Download stopped by user. {post_count} posts downloaded.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()