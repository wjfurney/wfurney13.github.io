---
layout: article
---
<div class="tags" markdown="1">

**Make YouTube Usable (Again)** <br> [internet](/articles/tags/internet), [software](/articles/tags/software) 

</div>

* auto-gen TOC:
{:toc}
<a class="prev" href="/articles/2023/marg"> < </a>
<a class="next" href="/articles/2024/wwwtsql"> > </a>


<p>
            Have you ever noticed that YouTube is way worse than it used to be? It's time we got rid of YouTube shorts,
            sponsors, clickbait titles and thumbnails, and those <a class="inline"  target="_blank" 
                href="/articles/2023/marg">insane comments.</a> The goal of this post is to help you
            enhance YouTube so that it resembles the good old days... or at least makes it usable.
        </p>
<h2><a class="inline" target="_blank" href="https://www.youtube.com/watch?v=Sa47RKkZV8E"
                style="text-decoration: none">Warning</a></h2>

This post will help you install browser extensions. Browser extensions are a top threat vector for malicious software and often contain "anonymous" data collection routines about your browsing activity [^1]. You should only install browser extensions that <i>you</i> trust. I make no claims about the safety of these particular extensions. I would recommend having as few browser extensions as you can to minimize risk. I always ensure that they are open source, heavily utilized, and read through the source code and issues pages on Github. I would not install even an open source extension if the code looks obsfucated or is too complicated to understand -- or if there are concerning issues (be sure to check the closed issues as well). If in doubt about a browser extension, don't install it and move on.


## Remove YouTube Shorts

I don't think this type of short form content is good and so opt to remove it entirely. Note that the filter can be modified if you only want to remove shorts from the homepage or something like that. To do this we will make use of UBlock Origin's custom filter rules.  

- Copy the text of <a href = "https://raw.githubusercontent.com/gijsdev/ublock-hide-yt-shorts/master/list.txt">this filter rule</a>  
- Click on UBlock Origin in the extensions menu and select "settings" to open the dashboard  
- Select "My Filters" and paste in the filter list  
YouTube shorts should now be removed. For a step-by-step guide on this process check out this [great video](https://www.youtube.com/watch?v=Nfr0uIU2lDI) [^2].

## Reddit Comments for YouTube

As the old adage goes, the only thing worse than Reddit comments is YouTube comments. OK, maybe I just made that up, but I still think it's true. I've used two extensions for this in the past [Karamel](https://github.com/odensc/karamel) and [Reddit Comments for YouTube](https://github.com/Xyl-AU/Reddit-Comments-for-YouTube). Both seem to work well and give you an option to see all the reddit threads for a video as well as the YouTube comments.

## SponsorBlock
Not too long ago YouTube videos didn't have sponsors. Ajay's <a class="inline" target="_blank"  href="https://github.com/ajayyy/SponsorBlock">SponsorBlock</a> helps by crowdsourcing sponsored portions of videos (which seems to work really well) and auto-skipping them. It also has some other cool features, like skipping to highlights of the video and skipping intros and outros.

## De-Arrow 

By the same author as (and built on top of) SponsorBlock, <a class="inline"  target="_blank" href="https://github.com/ajayyy/DeArrow">De-Arrow</a> is another extension (currently in beta)that uses crowdsourcing to replace video titles and thumbnails with their crowdsourced equivalents or a fallback. There are lots of options here as well. For example, you can choose to replace uppercase words in titles with Title Case, remove all emojis from titles, replace thumbnails with random screenshots from the middle of the video, and more. Fair warning that this one seems to be a bit quirkier with the crowdsourcing than SponsorBlock. That makes sense when you consider that really only nerds are submitting title and thumbnail replacement suggestions, but hopefully it will trend toward a better experience when more users come onboard.

<hr>

## Update 6/9/2024
Also check out the <a class="inline"  target="_blank"  href="https://addons.mozilla.org/en-US/firefox/addon/youtube-addon/">Improve Tube</a> extension for some additional UI enhancement options. I haven't used this one long enough to officially recommend it though.<br><br>See <a class="inline"  target="_blank" href="https://gist.githubusercontent.com/wfurney13/a677938536ecfa1a2e787f4f4cbe497b/raw/1740838d0154f5ca4d79fc0349f603d4427da902/uofhidebuttons"> this gist</a> for additional uBlock origin filters to hide the Join, Thanks, Clip, Share, Save and Download buttons in the video player.

[^1]: List of emails [ajay] has received [about inserting malware into [his] extension](https://sponsor.ajay.app/emails/)
[^2]: Funny highlight from this video. "My thing with shorts is I feel like I get dumber every time I watch them". I couldn't agree more.
