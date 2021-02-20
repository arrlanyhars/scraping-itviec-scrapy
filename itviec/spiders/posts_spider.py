import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = {
        "https://itviec.com/it-jobs"
    }

    def parse_item(self, response):
        img = response.css('div.jd-photos ::attr(style)').getall()
        img = [imgx.replace("background-image: url(","") for imgx in img]
        img = [imgy.replace(");","") for imgy in img]
        skills = response.css("div.tag-list > a > span::text").getall()
        skills = [skillsx.replace("\n","") for skillsx in skills]
        item = {
            #documentation, background image
            "img" : img,
            #top
            "job_title" : response.css("h1.job_title::text").get().strip(),
            "skills" : skills,
            "salary" : response.css("div.salary.not-signed-in > a::text").get(),
            "address" : response.css("div.address__full-address > span::text").get(),
            #left
            "logo" : response.css("div.logo > a > img::attr(src)").get(),
            "company" : response.css("div.short > div::text").get(),
            "employee_level" : response.css("div.employer-info > div > p.gear-icon::text").get().strip(),
            "number_of_employees" : response.css("div.employer-info > div > p.group-icon::text").get().strip(),
            "country" : response.css("div.country-icon > span::text").get(),
            "working_date" : response.css("div.working-date > span::text").get(),
            "overtime" : response.css("div.overtime > span::text").get(),
            "more_jobs" : response.css("div.current-jobs.links > a::text").get(),
            #description
            "value" : response.css("div.job_reason_to_join_us > div > ul > li::text").getall(),
            "jobdesc" : ''.join(response.css("div.job_description ::text").getall()),
            "skills_and_exp" : ''.join(response.css("div.skills_experience ::text").getall()),
            "benefits" : ''.join(response.css("div.love_working_here ::text").getall())
        }
        yield item

    def parse(self, response):
        for post in response.css('div.job__description'):
            data = {
                'url' : post.css("div h2 a::attr(href)").get()
            }
            link = "https://itviec.com" + data.get("url")
            if link is not None:
                yield scrapy.Request(url=link, callback=self.parse_item)
        
        next_page = response.css("div.search-page__jobs-pagination > ul > li > a::attr(href)")[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)