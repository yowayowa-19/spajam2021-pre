package spajam.yowayowa.prespajam2021

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter

class WalkPagerAdapter(fm: FragmentActivity): FragmentStateAdapter(fm)  {
    private val res : List<Fragment> = listOf<Fragment>(
        WalkFragment1(),
        WalkFragment2(),
        WalkFragment3()
    )

    override fun createFragment(position: Int): Fragment {
        return res[position]
    }

    override fun getItemCount(): Int {
        return res.size
    }

}