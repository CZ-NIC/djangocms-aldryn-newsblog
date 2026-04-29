const initSelection = (select) => {
    let path, match
    path = select.dataset.value_url.replace(
        new RegExp(`/${select.dataset.placeholder}/`), `/(${select.dataset.pattern})/`)
    match = window.location.href.match(path)
    if (match) {
        select.value = match[1]
    } else {
        const join_select = document.querySelector(`select[name="${select.dataset.join_name}"]`)
        path = select.dataset.join_url.replace(
            new RegExp(`/${select.dataset.placeholder}/`), `/(?<value>${select.dataset.pattern})/`)
        path = path.replace(
            new RegExp(`/${join_select.dataset.placeholder}/`), `/(?<join>${join_select.dataset.pattern})/`)
        match = window.location.href.match(path)
        if (match) {
            select.value = match.groups.value
            join_select.value = match.groups.join
        }
    }
}

const redirectToListAccordingSelection = (e) => {
    const select = e.target
    const join_select = document.querySelector(`select[name="${select.dataset.join_name}"]`)
    let path
    if (join_select && join_select.value) {
        if (select.value) {
            path = select.dataset.join_url.replace(new RegExp(`/${select.dataset.placeholder}/`), `/${select.value}/`)
            path = path.replace(new RegExp(`/${join_select.dataset.placeholder}/`), `/${join_select.value}/`)
        } else {
            path = join_select.dataset.value_url.replace(
                new RegExp(`/${join_select.dataset.placeholder}/`), `/${join_select.value}/`)
        }
    } else {
        if (select.value) {
            path = select.dataset.value_url.replace(new RegExp(`/${select.dataset.placeholder}/`), `/${select.value}/`)
        } else {
            path = select.dataset.list_url
        }
    }
    window.location.href = path
}

export const selectYearAndCategory = () => {
    for (const plugin of document.querySelectorAll(
        'select[name=aldryn_newsblog_category],select[name=aldryn_newsblog_year]')) {
        initSelection(plugin)
    }
    for (const plugin of document.querySelectorAll(
        'select[name=aldryn_newsblog_category],select[name=aldryn_newsblog_year]')) {
        plugin.addEventListener('change', redirectToListAccordingSelection)
    }
}
