export const hideMonthYearLinks = (query) => {
    for (const plugin of document.querySelectorAll('.aldryn-newsblog-month-year-links')) {
        const years = new Set()
        for (const article of document.querySelectorAll(query)) {
            years.add(article.dataset.year)
        }
        for (const link of plugin.getElementsByTagName('a')) {
            if (!years.has(link.dataset.year)) {
                link.style.display = 'none'
            }
        }
    }
}
