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
posts = []
dates = []
for k, post in enumerate(glob(os.path.join(root, "json/*.json"))):

    # Grab the contents
    with open(post, "r") as f:
        post_dict = json.load(f)

    # Generate the url
    date = dateparser.parse(post_dict["post"]["date"])
    date_str = "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day)
    date_str_tiny = date_str[2:]
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rss_date = "{:s}, {:d} {:s} {:d} 00:00:00 GMT".format(
        weekdays[date.weekday()], date.day, months[date.month - 1], date.year
    )
    post_dict["post"]["url"] = "{:s}.html".format(date_str)

    # Add metadata
    post_dict["post"]["shortdate"] = date_str
    post_dict["post"]["shortdate_tiny"] = date_str_tiny
    post_dict["post"]["rss_date"] = rss_date
    post_dict["post"]["id"] = date_str.replace("-", "_")
    post_dict["post"]["title_tiny"] = post_dict["post"].get(
        "title_tiny", post_dict["post"]["title"]
    )
    post_dict["post"]["social_image"] = post_dict["post"].get(
        "social_image", post_dict["post"]["banner"]
    )
    post_dict["post"]["rss_summary"] = post_dict["post"].get(
        "rss_summary", post_dict["post"]["summary"]
    )

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
        elif type(item) is dict:
            # Image / video / math
            idstr = item.get("id", "")
            if len(idstr):
                idstr = "id='{:s}'".format(idstr)
            IMAGE_EXTS = ["jpg", "gif", "png"]
            VIDEO_EXTS = ["mp4"]
            MATH_EXTS = ["tex"]
            CODE_EXTS = ["py"]
            if any([item.get("src", "").endswith(ext) for ext in IMAGE_EXTS]):
                media = """
                <div class="blog-image-container {:s}">
                    <img src='{:s}' style='width:100%;'></img>
                </div>
                """.format(
                    " ".join(item.get("css_classes", [])), item.get("src", "")
                )
            elif any([item.get("src", "").endswith(ext) for ext in VIDEO_EXTS]):
                media = """
                <div class="blog-image-container {:s}">
                <video width='100%' autoplay muted loop>
                    <source src='{:s}' type='video/mp4'>
                    Your browser does not support the video tag.
                </video>
                </div>""".format(
                    " ".join(item.get("css_classes", [])), item.get("src", "")
                )
            elif any([item.get("src", "").endswith(ext) for ext in MATH_EXTS]):
                with open(item["src"], "r") as f:
                    tex = f.read()
                # HACK
                tex = tex.replace(
                    "\\begin{align}",
                    "</p><p style='overflow-x: scroll;'>\\begin{align}",
                )
                tex = tex.replace("\\end{align}", "\\end{align}</p><p>")
                text += """
                <p class="math {:s}" {:s}>
                    {:s}
                </p> 
                """.format(
                    " ".join(item.get("css_classes", [])), idstr, tex
                )
                continue
            elif any([item.get("src", "").endswith(ext) for ext in CODE_EXTS]):
                with open(item["src"], "r") as f:
                    code = f.read()
                text += """<pre><code class='{:s}' {:s}>{:s}</code></pre>
                """.format(
                    " ".join(item.get("css_classes", [])), idstr, code
                )
                continue
            else:
                raise ValueError("")
            if len(item.get("caption", "")) == 0:
                text += """
                <div class="blog-image {:s}" {:s}>
                    {:s}
                </div> 
                """.format(
                    " ".join(item.get("css_classes", [])), idstr, media
                )
            else:
                text += """
                <div id="Figure{:d}Modal" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-body {:s}">
                                {:s}
                                <p>
                                    <span style="font-weight: 600; padding-right: 0.5em;">Figure {:d}</span>
                                    <span>{:s}</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="Figure{:d}" class="blog-image {:s}">
                    <a href="#" data-toggle="modal" data-target="#Figure{:d}Modal">
                        {:s}
                    </a>
                    <p>
                        <span style="font-weight: 600; padding-right: 0.5em;">Figure {:d}</span>
                        <span>{:s}</span>
                    </p>
                </div>
                """.format(
                    fignum,
                    " ".join(item.get("css_classes", [])),
                    media,
                    fignum,
                    item.get("caption", ""),
                    fignum,
                    " ".join(item.get("css_classes", [])),
                    fignum,
                    media,
                    fignum,
                    item.get("caption", ""),
                )
                fignum += 1
        else:
            raise ValueError("")

    post_dict["post"]["text"] = text

    # Append to the running list
    if post_dict["post"]["publish"]:
        dates.append(date_str)
        posts.append(post_dict)

# Sort the posts in reverse chronological order
posts = [post for _, post in sorted(zip(dates, posts))][::-1]

# Update the main page
template = env.get_template("index.html.jinja")
with open(os.path.join(root, "index.html"), "w") as f:
    f.write(template.render(posts=posts))

# Write the posts
template = env.get_template("post.html.jinja")
for k in range(len(posts)):

    # Write the html file
    with open(os.path.join(root, posts[k]["post"]["url"]), "w") as f:

        if k < len(posts) - 1:
            posts[k]["post"]["previous"] = posts[k + 1]["post"]["url"]
        else:
            posts[k]["post"]["previous"] = ""
        if k > 0:
            posts[k]["post"]["next"] = posts[k - 1]["post"]["url"]
        else:
            posts[k]["post"]["next"] = ""

        f.write(template.render(**posts[k]))

# Update the rss feed
template = env.get_template("rss.xml.jinja")
with open(os.path.join(root, "rss.xml"), "w") as f:
    f.write(template.render(posts=posts))
