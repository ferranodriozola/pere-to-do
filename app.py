# -*- coding: utf-8 -*-
# Copyright 2024-2025 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from dataclasses import dataclass, field
import uuid

st.set_page_config(page_title="Tasques Ovidi", page_icon=":memo:")

# Declare alias for st.session_state, just for convenience.
state = st.session_state


@dataclass
class Todo:
    text: str
    is_done: bool = False
    uid: uuid.UUID = field(default_factory=uuid.uuid4)


text = """
(X)Omplir excel Puteolanus
Generar xml Puteolanus
Corregir manualment xml Puteolanus

Creador xml personatges
*csv persones drive
*csv llocs drive
*db drive (occupation)
*db drive (certainty)
*gestionar db en línea amb el generador xml normal en local:
*db drive (languages) (!!)
*db drive (city) (!!)
*db drive (country) (!!)
*fer python persones
*fer python llocs
"""


def converteix_text_a_todos(text: str) -> list[Todo]:
    todos = []

    for raw_line in text.strip("\n").splitlines():
        line = raw_line.strip()
        is_done = line.startswith("(X)")

        if is_done:
            line = line[3:].lstrip()

        todos.append(Todo(text=line, is_done=is_done))

    return todos


text_cuinat = converteix_text_a_todos(text)

if "todos" not in state:
    state.todos = text_cuinat


def remove_todo(i):
    state.todos.pop(i)


def check_todo(i, new_value):
    state.todos[i].is_done = new_value


def delete_all_checked():
    state.todos = [t for t in state.todos if not t.is_done]


with st.container(horizontal_alignment="center"):
    st.title(
        ":orange[:material/checklist:] Tasques Ovidi",
        width="content",
        anchor=False,
    )


with st.container(horizontal=True, horizontal_alignment="center"):
    st.button(
        ":small[Delete all checked]",
        icon=":material/delete_forever:",
        type="tertiary",
        on_click=delete_all_checked,
        disabled=not state.todos,
    )


if state.todos:
    with st.container(gap=None, border=True):
        for i, todo in enumerate(state.todos):
            with st.container(horizontal=True, vertical_alignment="center"):
                st.checkbox(
                    todo.text,
                    value=todo.is_done,
                    width="stretch",
                    on_change=check_todo,
                    args=[i, not todo.is_done],
                    key=f"todo-chk-{todo.uid}",
                )
                st.button(
                    ":material/delete:",
                    type="tertiary",
                    on_click=remove_todo,
                    args=[i],
                    key=f"delete_{i}",
                )

else:
    st.info("No to-do items. Go fly a kite! :material/family_link:")
