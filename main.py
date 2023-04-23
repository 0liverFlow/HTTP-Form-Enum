import argparse
import re
from bs4 import BeautifulSoup as bsoup

from webinspect import WebInspect

from rich import print as printc
from rich.table import Table


headers = {
    "DNT": "1",
    "Accept-encoding": "gzip, deflate, br",
    "Referer": "https://www.it-connect-fr/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",

}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main.py', description='Webpage source code enumeration tool', epilog='Ping me: 0liverFlow@proton.me')
    parser.add_argument('-u','--url', metavar="URL", help="target's url (e.g. https://example.com)", required=True)
    args = parser.parse_args()
    url = args.url


    inspected_webpage = WebInspect(url, headers)
    ##############################
    # Checking website language
    ##############################
    printc(f"\n[u][yellow1 b][*][/yellow1 b] LANGUAGE[/u]")
    inspected_webpage.get_language()
    if not inspected_webpage.language is None:
        printc(f"[green1 b][+][/green1 b] Language found: {inspected_webpage.language}")
    else:
        printc(f"[red1 b][red1 b][-][/red1 b][/red1 b] Language: N/A")

    #########################
    # Checking website title
    #########################
    inspected_webpage.get_title()
    printc(f"\n[u][yellow1 b][*][/yellow1 b] TITLE[/u]")
    if not inspected_webpage.title is None:
        printc(f"\n[green1 b][+][/green1 b] Title found: {inspected_webpage.title}")
    else:
        printc(f"\n[red1 b][-][/red1 b] Title: N/A")

    #####################
    # Checking comments
    #####################
    inspected_webpage.get_comments()
    printc(f"\n[u][yellow1 b][*][/yellow1 b] COMMENTS[/u]")
    if not inspected_webpage.comments is None:
        table = Table(title=f"{inspected_webpage.double_letter_format('Comments Found')}", style="bold", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Value", justify="center")
        for commment_id, comment_value in enumerate(inspected_webpage.comments, start=1):
            if comment_value:
                table.add_row(str(commment_id), re.sub('\s\s+',' ', comment_value.strip()))
                print(re.sub('\s\s+',' ', comment_value.strip()))
    else:
        printc("[red1 b][-][/red1 b] Comments: N/A")

    ###############################
    # Checking website's meta tags
    ###############################
    inspected_webpage.get_meta_tags()
    printc(f"\n[u][yellow1 b][*][/yellow1 b] META TAGS[/u]")
    meta_tags_names = ["generator", "twitter", "robots", "keywords"]
    meta_tags_properties = ["fb:", "twitter:", "article:publisher", "article:published_time", "article:modified_time", "og:description", "og:type"]
    if not inspected_webpage.meta_tags is None:
        printc(f"[u][green1 b][+][/green1 b] Meta tags found![/u]")
        table = Table(title=f"{inspected_webpage.double_letter_format('Meta Tags')}", style="bold", show_lines=True)
        table.add_column("Name/Property", justify="center")
        table.add_column("Value", justify="center")
        for meta_tag in inspected_webpage.meta_tags:
            if meta_tag.has_attr('name'):
                for meta in meta_tags_names:
                    if re.search(f"^{meta}", meta_tag['name'], flags=re.I):
                        table.add_row(f"{meta_tag['name']}", f"{meta_tag['content']}")
                        break
            elif meta_tag.has_attr('property'):
                for meta in meta_tags_properties:
                    if re.search(f"^{meta}", meta_tag['property'], flags=re.I):
                        table.add_row(f"{meta_tag['name']}", f"{meta_tag['content']}")
                        break
        printc(table)
    else:
        printc("[red1 b][-][/red1 b] Meta Tags: N/A")
    
    #################
    # Hidden Inputs
    #################
    inspected_webpage.get_hidden_inputs()
    printc(f"\n[u][yellow1 b][*][/yellow1 b] HIDDEN INPUTS[/u]")
    if not inspected_webpage.hidden_inputs is None:
        printc('[green1 b][+][/green1 b] Hidden inputs found!')
        table = Table(title=f"{inspected_webpage.double_letter_format('Hidden Inputs')}", style="bold", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Value", justify="center")
        for hidden_input_id, hidden_input_tag in enumerate(inspected_webpage.hidden_inputs):
            table.add_row(f"{hidden_input_id}", f"{hidden_input_tag}")
        printc(table)
    else:
        printc("[red1 b][-][/red1 b] Hidden input: N/A")
    
    #######################
    # Display None Tags
    #######################
    inspected_webpage.get_display_none_tags()
    if not inspected_webpage.display_none is None:
        printc("[green1 b][+][/green1 b] Hidden elements found!")
        table = Table(title=f"{inspected_webpage.double_letter_format('Display None')}", style="bold", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Value", justify="center")
        for display_none_id, display_none_tag in enumerate(inspected_webpage.display_none, start=1):
            table.add_row(f"{display_none_id}", f"{display_none_tag}")
        printc(table)
    else:
        printc("[red1 b][-][/red1 b] Display none tags: N/A")

    #####################
    # Looking for forms
    #####################
    inspected_webpage.get_forms()
    if not inspected_webpage.forms is None:
        printc("[green1 b][+][/green1 b] Forms found!")
        #print(inspected_webpage.forms)
        for form_num, form in enumerate(inspected_webpage.forms, start=1):
            form_title = "Form n°" + str(form_num)
            table = Table(title=f"{inspected_webpage.double_letter_format(form_title)}", show_lines=True)
            table.add_column("Attribute", justify="center")
            table.add_column("Value", justify="center", max_width=70)
            for attr,value in form.attrs.items():
                #print('I AM HERE')
                table.add_row(f"{attr}", f"{value}")
            printc(table)
            print()
            inputs = form.find_all("input")
            if len(inputs):
                form_inputs_title = form_title + "'s inputs"
                table = Table(title=f"{inspected_webpage.double_letter_format(form_inputs_title)}", show_lines=True)
                table.add_column("ID", justify="center")
                table.add_column("Value", justify="center", max_width=70)
                for input_id, input_tag in enumerate(inputs, start=1):
                    #print('I CAME HERE')
                    table.add_row(f"{input_id}", f"{input_tag}")
                printc(table)
            print(f"{'-'*100}")
    else:
        printc("[red1 b][-][/red1 b] No forms found!")
    """
    ################            
    # Robots.txt
    ################
    inspected_webpage.get_robots_txt()
    print(f"\n[u][yellow1 b][*][/yellow1 b] Robots.txt[/u]")
    if not inspected_webpage.robots_txt is None:
        printc("[u][green1 b][+][/green1 b] robots.txt file found![/u]")
        table = Table(title=f"{inspected_webpage.double_letter_format('Robots.txt')}", style="bold", show_lines=True)
        for robots_txt_rule in inspected_webpage.robots_txt:
            if not re.search("^(Disallow|User-agent|Sitemap)", robots_txt_rule.strip(), flags=re.IGNORECASE) is None:
                table.add_row(f"{robots_txt_rule.strip()}")
    else:
        printc("[red1 b][-][/red1 b] Robots.txt does not exist!")

    ##################
    # Phpinfo
    ##################
    inspected_webpage.get_phpinfo()
    print(f"[u][yellow1 b][*][/yellow1 b] PHP INFO[/u]")
    if not inspected_webpage.phpinfo is None:
        printc(f"[green1 b][+][/green1 b] phpinfo.php found!")
        try:
            phpinfo_soup = bsoup(inspected_webpage.phpinfo, 'html.parser')
            php_version = inspected_webpage.phpinfo.find_all("h1", class_="p")[0].string
            printc(f"[green1 b][+][/green1 b] PHP running version: {php_version.split()[-1]}")
        except BaseException:
            pass
    

    ##################
    # Cgidir
    ##################
    inspected_webpage.getcgidir()
    print(f"[u][yellow1 b][*][/yellow1 b] CGI_DIR[/u]")
    if not inspected_webpage.cgidir is None:
        print(f"[green1 b][+][/green1 b] {inspected_webpage.cgidir} found!")
    """