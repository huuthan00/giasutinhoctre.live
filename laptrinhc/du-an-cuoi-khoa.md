# Du an cuoi khoa

Hoc sinh chon 1 du an. Moi du an can co menu, toi thieu 5 ham rieng, va co phan kiem tra du lieu nhap.

## De tai 1: Game doan so nang cap

Tinh nang bat buoc:

- Chon muc do: de, vua, kho.
- Gioi han so lan doan theo muc do.
- Bao lon hon, nho hon sau moi lan doan.
- Tinh diem dua tren so lan doan.
- Cho choi lai.

Tinh nang mo rong:

- Luu diem cao nhat vao file.
- Them goi y sau 3 lan sai.

## De tai 2: Quan ly diem hoc sinh

Tinh nang bat buoc:

- Them hoc sinh gom ten va diem.
- Xem danh sach.
- Tim hoc sinh theo ten.
- Sap xep theo diem.
- Tinh diem trung binh, diem cao nhat, diem thap nhat.

Tinh nang mo rong:

- Luu danh sach ra file.
- Doc danh sach tu file khi mo chuong trinh.

## De tai 3: Tu dien mini

Tinh nang bat buoc:

- Them tu moi gom tu tieng Anh va nghia tieng Viet.
- Tim tu.
- Xem tat ca tu.
- Xoa tu.
- Dem so tu trong tu dien.

Tinh nang mo rong:

- Luu va doc tu dien bang file text.
- Tim gan dung theo mot phan cua tu.

## De tai 4: Caro console 3x3

Tinh nang bat buoc:

- Ban co 3x3.
- Hai nguoi choi lan luot danh X va O.
- Kiem tra thang, hoa.
- Khong cho danh vao o da co quan.
- Cho choi lai.

Tinh nang mo rong:

- Dem ti so X thang, O thang, hoa.
- Them may choi ngau nhien.

## De tai 5: Quan ly viec can lam

Tinh nang bat buoc:

- Them viec.
- Xem viec chua xong va da xong.
- Danh dau hoan thanh.
- Xoa viec.
- Tim viec theo tu khoa.

Tinh nang mo rong:

- Luu danh sach vao file.
- Them muc do uu tien.

## Tieu chi cham du an

| Tieu chi | Diem |
| --- | ---: |
| Co day du tinh nang bat buoc | 3 |
| Chuong trinh chay on dinh, it loi | 2 |
| Code tach ham ro rang | 2 |
| Biet xu ly du lieu nhap sai | 1 |
| Output de dung, menu de hieu | 1 |
| Trinh bay du an mach lac | 1 |

## Mau cau truc code

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

void showMenu() {
    cout << "===== MENU =====\n";
    cout << "1. Chuc nang 1\n";
    cout << "2. Chuc nang 2\n";
    cout << "0. Thoat\n";
}

int main() {
    int choice;

    do {
        showMenu();
        cout << "Chon: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Dang lam chuc nang 1\n";
                break;
            case 2:
                cout << "Dang lam chuc nang 2\n";
                break;
            case 0:
                cout << "Tam biet!\n";
                break;
            default:
                cout << "Lua chon khong hop le.\n";
        }
    } while (choice != 0);

    return 0;
}
```

