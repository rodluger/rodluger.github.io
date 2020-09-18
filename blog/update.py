from jinja2 import Environment, FileSystemLoader
import os
import json
from glob import glob
import dateparser

root = os.path.dirname(os.path.abspath(__file__))

# Remove all .html files
for file in glob(os.path.join(root, "*.html")):
    os.remove(file)

# Render the individual posts
templates_dir = os.path.join(root, "templates")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template("post.html.jinja")
posts = []
dates = []
for k, post in enumerate(glob(os.path.join(root, "json/*.json"))):

    # Grab the contents
    with open(post, "r") as f:
        post_dict = json.load(f)

    # Generate the url
    date = dateparser.parse(post_dict["post"]["date"])
    date_str = "{:02d}-{:02d}-{:04d}".format(date.day, date.month, date.year)
    post_dict["post"]["url"] = "{:s}.html".format(date_str)

    # Add metadata
    post_dict["post"]["shortdate"] = date_str
    post_dict["post"]["id"] = date_str.replace("-", "_")

    # Disqus metadata
    post_dict["post"]["disqus"] = {}
    post_dict["post"]["disqus"]["url"] = "https://luger.dev/blog/{:s}".format(
        post_dict["post"]["url"]
    )
    post_dict["post"]["disqus"]["identifier"] = date_str

    # Format the contents
    text = "<p>{:s}</p>".format(post_dict["post"]["summary"])
    fignum = 1
    for item in post_dict["post"]["contents"]:
        if type(item) is str:
            # Regular text
            text += "<p>{:s}</p>".format(item)
        elif type(item) is list:
            # Image
            url, caption = item
            text += """
            <div style='text-align: center; width:75%; margin-left: auto; margin-right:auto; margin-bottom: 30px;'>
                <a href='{:s}'><img src='{:s}' style='width:100%;'></img></a>
                <p>
                <span style='font-weight: 600; padding-right: 0.5em;'>Figure {:d}</span>
                <span>{:s}</span>
                </p>
            </div>
            """.format(
                url, url, fignum, caption
            )
            fignum += 1

    post_dict["post"]["text"] = text

    # Write the html file
    with open(os.path.join(root, post_dict["post"]["url"]), "w") as f:
        f.write(template.render(**post_dict))

    # Append to the running list
    dates.append(date_str)
    posts.append(post_dict)

# Sort the posts in reverse chronological order
posts = [post for _, post in sorted(zip(dates, posts))][::-1]

# Update the main page
template = env.get_template("index.html.jinja")
with open(os.path.join(root, "index.html"), "w") as f:
    f.write(template.render(posts=posts))
