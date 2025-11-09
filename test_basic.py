#!/usr/bin/env python3
"""
Basic functionality tests for ReproductorAlecksey
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test main modules
        import reproductor
        print("  ✅ reproductor.py imports successfully")
    except Exception as e:
        print(f"  ❌ reproductor.py import failed: {e}")
        return False
    
    try:
        import audio_visualizer
        print("  ✅ audio_visualizer.py imports successfully")
    except Exception as e:
        print(f"  ❌ audio_visualizer.py import failed: {e}")
        return False
    
    try:
        import audio_enhancer
        print("  ✅ audio_enhancer.py imports successfully")
    except Exception as e:
        print(f"  ❌ audio_enhancer.py import failed: {e}")
        return False
    
    try:
        import web_ui
        print("  ✅ web_ui.py imports successfully")
    except Exception as e:
        print(f"  ❌ web_ui.py import failed: {e}")
        return False
    
    try:
        import launcher
        print("  ✅ launcher.py imports successfully")
    except Exception as e:
        print(f"  ❌ launcher.py import failed: {e}")
        return False
    
    return True

def test_dependencies():
    """Test that required dependencies are available"""
    print("\n🧪 Testing dependencies...")
    
    dependencies = {
        'rich': 'Terminal UI formatting',
        'pygame': 'Audio visualization',
        'numpy': 'Audio processing',
        'pydub': 'Audio conversion',
        'flask': 'Web UI',
        'flask_cors': 'Web UI CORS',
    }
    
    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {module} ({description})")
        except ImportError:
            print(f"  ⚠️  {module} not installed ({description})")
            all_ok = False
    
    return all_ok

def test_ytdlp():
    """Test that yt-dlp is available"""
    print("\n🧪 Testing yt-dlp...")
    
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"  ✅ yt-dlp version {version}")
        return True
    except:
        print("  ⚠️  yt-dlp not installed")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n🧪 Testing directories...")
    
    downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
    
    if downloads_dir.exists():
        print(f"  ✅ Downloads directory exists: {downloads_dir}")
        return True
    else:
        print(f"  ℹ️  Downloads directory will be created on first use: {downloads_dir}")
        return True

def test_security():
    """Test security features"""
    print("\n🧪 Testing security features...")
    
    try:
        from web_ui import VideoDownloader
        downloader = VideoDownloader()
        
        # Test valid URLs
        valid_urls = [
            'https://www.youtube.com/watch?v=example',
            'http://example.com/video'
        ]
        
        for url in valid_urls:
            if downloader.validate_url(url):
                print(f"  ✅ Valid URL accepted: {url[:40]}...")
            else:
                print(f"  ❌ Valid URL rejected: {url[:40]}...")
                return False
        
        # Test invalid URLs
        invalid_urls = [
            'javascript:alert(1)',
            'file:///etc/passwd',
            'https://example.com; rm -rf /',
            'https://example.com && malicious',
            'https://example.com | cat /etc/passwd',
        ]
        
        for url in invalid_urls:
            if not downloader.validate_url(url):
                print(f"  ✅ Invalid URL rejected: {url[:40]}...")
            else:
                print(f"  ❌ Dangerous URL accepted: {url[:40]}...")
                return False
        
        print("  ✅ URL validation working correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ Security test failed: {e}")
        return False

def test_neon_colors():
    """Test that neon colors are defined"""
    print("\n🧪 Testing neon theme...")
    
    try:
        import reproductor
        colors = reproductor.NEON_COLORS
        
        expected_colors = ['pink', 'cyan', 'green', 'yellow', 'orange', 'purple', 'blue']
        for color in expected_colors:
            if color in colors:
                print(f"  ✅ Neon color '{color}' defined: {colors[color]}")
            else:
                print(f"  ❌ Neon color '{color}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Neon theme test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🎵 ReproductorAlecksey - Test Suite")
    print("=" * 60)
    
    results = {
        'Imports': test_imports(),
        'Dependencies': test_dependencies(),
        'yt-dlp': test_ytdlp(),
        'Directories': test_directories(),
        'Security': test_security(),
        'Neon Theme': test_neon_colors(),
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed or dependencies are missing")
        print("   Run: python install.py to install missing dependencies")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
