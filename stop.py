def print_hero():
    # 基础打印
    print("王贺祥天下无敌")
    
    # 艺术字效果
    art = r"""
    ┌─┐┬  ┬┌─┐┬─┐┬┌─┐┌┬┐
    ├─┤└┐┌┘├┤ ├┬┘│├─┘ │ 
    ┴ ┴ └┘ └─┘┴└─┴┴   ┴ 
    """
    print(art)
    
    # 逐字打印效果
    text = "王贺祥天下无敌"
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.2)
    print()
    
    # 彩色打印
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    reset = '\033[0m'
    
    for i, char in enumerate(text):
        print(f"{colors[i % len(colors)]}{char}{reset}", end='')
    print()
    
    # 边框效果
    border = "★" * 20
    print(border)
    print(f"★       {text}       ★")
    print(border)

if __name__ == "__main__":
    import time
    
    print("=" * 50)
    print("王贺祥天下无敌 - 特别致敬程序")
    print("=" * 50)
    
    print_hero()
    
    # 额外致敬
    print("\n附加致敬:")
    print("王者风范显神威")
    print("贺喜声中赞英雄")
    print("祥瑞之光耀八方")
    print("天地为之动容色")
    print("下凡英雄独此尊")
    print("无敌传说永流传")