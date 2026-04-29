export const hideMonthYearLinks = () => {
    for (const plugin of document.querySelectorAll('.aldryn-newsblog-month-year-links')) {
        const years = new Set()
        for (const article of document.querySelectorAll('.djangocms-newsblog-article-list .c-article')) {
            years.add(article.dataset.year)
        }
        for (const link of plugin.getElementsByTagName('a')) {
            if (!years.has(link.dataset.year)) {
                link.style.display = 'none'
            }
        }
    }
}
